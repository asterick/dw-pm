from struct import unpack
import sys, re

# Not listed:
# @SPLT
# @CALL
6# ?

FUNCTIONS = {
	0x90: "<<",
	0x91: ">>",
	0x92: "@UDEF2",
	0x93: "@DUPL",
	0x94: "@EXCH",
	0x95: "@UDEF5",
	0x96: "@UDEF6",
	0x97: "@UDEF7",
	0x98: "@UDEF8",
	0x99: "@UDEF9",
	0x9A: "@UDEFA",
	0x9B: "@UDEFB",
	0x9C: "@UDEFC",
	0x9D: "@UDEFD",
	0x9E: "@UDEFE",
	0x9F: "@UDEFF",

	# FUNCTIONS
	0xA0: "@F",
	0xA1: "@T",
	0xA2: "@ABS",
	0xA3: "@NEG",
	0xA4: "@NOT",
	0xA5: "+",
	0xA6: "-",
	0xA7: "/",
	0xA8: "*",
	0xA9: "@MAX",
	0xAA: "@MIN",
	0xAB: "@MOD",
	0xAC: "<",
	0xAD: ">",
	0xAE: "=",
	0xAF: "!=",
	0xB0: "@AND",
	0xB1: "@OR",
	0xB2: "@XOR",
	0xB3: "@EXT",
	0xB4: "@INS",
	0xB5: "@ERR",
	0xB6: "@IF",
	0xB7: "@ELSE",
	0xB8: "@ENDIF",
	0xB9: "@ISDEF",
	0xBE: "(",
	0xBF: ")"
}

class Decoder:
	def __init__(self, fo):
		self.fo = fo

	def commands(self):
		while True:
			code = self.expect("Command")

			# Module Level Commands
			if code == 0xE0:
				yield ('MB', self.string(), self.string())
			elif code == 0xE1:
				yield ('ME', )
				break
			elif code == 0xEB:
				yield ('DT', self.numbers())
			elif code == 0xEC:
				yield ('AD', self.number(), self.number(), self.letter())

			# Comment and Checksum Command
			elif code == 0xEA:
				yield ('CO', self.number(), self.string())

			# Sections
			elif code == 0xE5:
				yield ('SB', self.number())
			elif code == 0xE6:
				yield ('ST', self.number(), self.section_types(), self.string(), self.numbers())
			elif code == 0xE7:
				yield ('SA', self.number(), self.term(), self.term())

			# Symbolic Name Declaration and Type Definition
			elif code == 0xE8:
				yield ('NI', 'I%i' % self.number(), self.string())
			elif code == 0xE9:
				yield ('NX', 'X%i' % self.number(), self.string())
			elif code == 0xF0:
				yield ('NN', 'N%i' % self.number(), self.string())
			elif code == 0xF1:
				yield ('AT', self.variable(), self.number(), self.number(), self.numbers())
			elif code == 0xF2:
				yield ('TY', self.number(), self.list("Variable", "Number"))

			# Value Assignment
			elif code == 0xE2:
				yield ('AS', self.variable(), self.expression())
			
			# Loading Commands
			elif code == 0xED:
				yield ('LD', self.string())
			elif code == 0xE3:
				yield ('IR', self.letter(), self.number(), self.number())
			elif code == 0xE4:
				yield ('LR', self.expressions())
			elif code == 0xF7:
				yield ('RE', self.term())

			# Linkage Commands
			elif code == 0xF3:
				yield ('RI', "I%i" % self.number(), self.number())
			elif code == 0xF4:
				yield ('WX', "W%i" % self.number(), self.term())
			elif code == 0xF5:
				yield ('LI', self.string(), self.string())
			elif code == 0xF6:
				yield ('LX', "X%i" % self.number(), self.string())


			#elif code == 0xEE:
			#	yield ('CS(S)',)
			#elif code == 0xEF:
			#	yield ('CS',)
			elif code == 0xF8:
				yield ('SC', self.number(), self.number(), self.string(), self.expressions())
			elif code == 0xF9:
				yield ('LN', self.numbers())
			else:
				print ("UNKNOWN COMMAND %02X" % code)

	def byte(self):
		return ord(self.fo.read(1))

	def type(self):
		code = self.byte()

		if code <= 0x8F:
			return "Number"
		elif code >= 0x90 and code <= 0xBF:
			return "Function"
		elif code >= 0xC1 and code <= 0xDA:
			return "Letter"
		elif code >= 0xE0 and code <= 0xF9:
			return "Command"
		else:
			return "Undefined"

	def peek(self):
		before = self.fo.tell()
		type = self.type()
		self.fo.seek(before)

		return type

	def expect(self, *types):
		type = self.peek()

		if "Variable" in types and type == "Letter":
			type = "Variable"

		if not type in types:
			raise Exception("Expected %s: got %s" % (', '.join(types), type))

		translate = {
			"Command": self.byte,
			"Function": self.function,
			"Number": self.number,
			"Letter": self.letter,
			"Variable": self.variable
		}

		return translate[type]()


	# Lists
	def list(self, *types):
		terms = []
		
		while True:
			before = self.fo.tell()
			try:
				terms += [self.expect(*types)]
			except:
				self.fo.seek(before)
				return terms

	def section_types(self):
		terms = []

		while self.peek() == "Letter":
			l = self.expect("Letter")

			if l == "Y":
				terms += [l + str(self.number())]
			else:
				terms += [l]

		return terms


	def letters(self):
		return self.list("Letter")

	def numbers(self):
		return self.list("Number")

	def expressions(self):
		return self.expression()

	# Atomics
	def term(self):
		return self.expect("Function", "Number", "Variable")

	def variable(self):
		prefix = self.letter()

		if prefix in "LPRS":
			suffix = self.number()
			if suffix:
				return prefix + str(suffix)
			else:
				return prefix
		elif prefix in "INWXT":
			return prefix + str(self.number())
		elif prefix == "G":
			return prefix
		else:
			return prefix
			raise Exception("Expected a variable")

	def expression(self, top = True):
		return self.list("Variable", "Number", "Function")

	def function(self):
		code = self.byte()

		if not code in FUNCTIONS:
			raise Exception("Expected a function")

		return FUNCTIONS[code]

	def letter(self):
		code = self.byte()

		if code >= 0xC1 and code <= 0xDA:
			return	chr(ord('A') + code - 0xC1)
		else:
			raise Exception("Expected a letter")

	def number(self):
		code = self.byte()

		if code <= 0x7F:
			return code
		elif code == 0x80:
			return None
		elif code <= 0x8F:
			return sum([v << (i * 8) for i, v in enumerate(self.fo.read(code - 0x80)[::-1])])
		else:
			raise Exception("Expected a number")

	def string(self):
		return self.fo.read(self.number())

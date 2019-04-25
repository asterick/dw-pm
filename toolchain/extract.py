import sys
import re

def chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def symbols(fn):
	with open(fn, "r") as fo:
		while not re.search(r'^Symbols:', fo.readline()):
			pass

		for _ in range(2):
			fo.readline()

		for line in fo.readlines():
			match = re.search(r'([_a-zA-Z0-9]+) - 0x([0-9a-f]+)', line)

			if not match:
				break

			symbol, address = match.groups()
			
			yield symbol, int(address, 16)

bank = 0
binary = b'\xFF' * 0x200000
start, end = 0x2100, 0x2100

with open(sys.argv[-2], "wb") as fo:
	with open(sys.argv[-1], "r") as fi:
		for line in fi.readlines():
			match = re.search(r'^:(([0-9A-Fa-f]{2})([0-9A-Fa-f]{4})([0-9A-Fa-f]{2})([0-9A-Fa-f]*?))([0-9A-Fa-f]{2})$', line)
			
			checked, count, address, command, data, crc = match.groups()

			checked = [int(d, 16) for d in chunks(checked, 2)]
			crc = int(crc, 16)

			if 0xFF & -sum(checked) != crc:
				raise Exception('CRC failed on record')

			command = int(command, 16)
			count = int(count, 16)
			address = int(address, 16) + bank
			raw_data = bytes([int(d, 16) for d in chunks(data, 2)])


			if count != len(raw_data):
				raise Exception('Bad record')

			if command == 0x00:
				# Data at address
				end = max(end, address + count)
				start = min(start, address)

				binary = binary[:address] + raw_data + binary[address+count:]
			elif command == 0x04:
				# Entended address
				bank = int(data, 16) << 16
			elif command == 0x01:
				# End of file
				break
			else:
				raise Exception('Unknown command %02X' % command)

		for funct, address in symbols(sys.argv[-3]):
			match = re.search(r'_IRQHandler_([0-9a-fA-F]+)', funct)
			if not match:
				continue

			irq = int(match.group(1), 16)

			target = 0x2102 + (irq * 6)

			if target < 0x2108 or target >= 0x21A4:
				raise Exception('Illegal IRQ %02x' % irq)


			if (address & 0xFF8000) != 0: # Lower page
				# LD NB, bank(target)
				branch = b'\xCE\xC4' + (address >> 15).to_bytes(1)
			else:
				branch = b''


			# It's almsot garanteed that we will not be able to do a short branch, don't even bother checking
			delta = (address - target + len(branch) + 2) & 0xFFFF
			branch += b'\xF3' + delta.to_bytes(2, byteorder='little')

			print (branch)
			binary = binary[:target] + branch + binary[target+len(branch):]


		fo.write(binary[start:end])

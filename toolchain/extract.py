from mufom import Decoder

import sys

with open(sys.argv[-2], "wb") as fo:
	with open(sys.argv[-1], "rb") as fi:
		decoder = Decoder(fi)

		for command in decoder.commands():
			print (command)
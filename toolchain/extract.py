import sys
import re

def chunks(l, n): 
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

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

			if (0xFF & -sum(checked) ^ crc) != 0:
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

		fo.write(binary[start:end])

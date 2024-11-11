# 1.0.0.0:
# - support for fs25


import os

os.system('color 0E')

print("===========================")
print("L64 Decoder 1.0.0.0")
print("===========================")

baseDirectory = os.path.dirname(os.path.realpath(__file__)) + '\\l64\\'

if not os.path.exists(baseDirectory):
	os.makedirs(baseDirectory, exist_ok=True)

ge10_key2 = [0x14, 0x0B, 0x09, 0x02, 0x08, 0x03, 0x03, 0x03]
ge10_key3 = [0x05, 0x0f, 0x0b, 0x01, 0x08, 0x02, 0x03, 0x03, 0x08, 0x04, 0x03, 0x01, 0x04, 0x07, 0x08, 0x14]

count = 0
errorCount = 0

def scanFile(path):
	file = open(path, "r+b")
	array = bytearray(file.read())

	shortPath = path.split(baseDirectory)[1]

	unknownFormat = False

	global count
	global errorCount

	if array[0] == 0x02 or array[0] == 0x03:
		if array[0] == 0x02:
			for i in range(2, len(array)):
				array[i] = (array[i] + (i - 0x01) + ge10_key2[(i - 0x01) & 0x07]) & 0xFF
		else:
			for i in range(2, len(array)):
				array[i] = (array[i] + i + ge10_key3[(i - 0x01) & 0x0F]) & 0xFF

		array[0] = 0x01
		array[1] = 0x03

		file.seek(0)
		file.write(array)
		file.close()

		count +=1

		filename, extension = os.path.splitext(path)
		os.rename(path, filename + ".lua")

		print('.l64: "{0}" unlocked!'.format(shortPath))
	elif array[0] == 0x01 and array[1] == 0x03:
		errorCount +=1
		print('.l64 "{0}" already unlocked!'.format(shortPath))
	else:
		unknownFormat = True

	if unknownFormat:
		errorCount +=1
		print('Unknown .l64 format: "{0}"'.format(shortPath))

def scanDir(src, subpath):
	srcDir = os.path.join(src, subpath)

	with os.scandir(srcDir) as it:
		for path in it:
			if path.name.endswith('.l64'):
				scanFile(os.path.join(srcDir, path.name))
			elif path.is_dir():
				scanDir(src, os.path.join(subpath, path.name))

scanDir(baseDirectory, '')

if count > 0:
	print('Successfully unlocked {0} files.'.format(count))

if errorCount > 0:
	print('Failed to unlock {0} files.'.format(errorCount))

os.system('pause')
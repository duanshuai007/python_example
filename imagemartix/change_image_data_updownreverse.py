import os
import sys

img = []
with open(sys.argv[1], "rb") as f:
	while True:
		line = f.read(81)
		if len(line) == 0:
			break
		litem = []
		for i in line:
			litem.append(i)
		litem.reverse()
		for i in litem:
			img.append(i)
img.reverse()
print(img)
with open("./output.bin", "wb") as f:
	f.write(bytes(img))

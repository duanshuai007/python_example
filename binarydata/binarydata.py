import random


cmd = []
body = []

ssid = "Frog"
password = "FrogsHealth@1"

body.append(0x01)
body.append(len(ssid))
for c in ssid:
#print("c:{} type:{}".format(c, type(c)))
    body.append(ord(c))
body.append(len(password))
for c in password:
#   print("c:{} type:{}".format(c, type(c)))
    body.append(ord(c))

for i in range(1, 16):
    body.append(i)

cmd.append(0x5a)
cmd.append(0x89)
cmd.append(len(body))
for i in body:
    cmd.append(i)

crc = 0 
for i in cmd:
    crc += i
crc &= 0xff
cmd.append(crc)
cmd.append(0xa5)

s = ""
for c in cmd:
    s = "{} {}".format(s, hex(c))
print(s)



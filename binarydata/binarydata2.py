import struct
import random

update_url = "http://baidu.com"
fmt = ">BBB{}s".format(len(update_url))
sendmsg = struct.pack(fmt, 0x5a, random.randint(0, 255), len(update_url), bytes(update_url, encoding="utf-8"))
verity = 0 
for i in sendmsg:
	print(i)
verity = verity + i 
verity &= 0xff
fmt_all = ">{}sBB".format(len(sendmsg))
sendmsg = struct.pack(fmt_all, sendmsg, verity, 0xa5)

print(sendmsg)


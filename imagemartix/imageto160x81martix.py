#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
from PIL import Image

IMAGE_WIDTH = 160
IMAGE_HEIGHT = 160

#fullscreen = True表示转换为160x160的目标大小
#keepshape = True表示按照比例放大或缩小图片
#返回的数据总是160x160的图片数据信息
def show_image_on_screen(filename:str, fullscreen:bool, keepshape:bool, rowreverse:bool, colreverse:bool):
	if not os.path.exists(filename):
		print("show_image_on_screen file[{}] not exists!".format(filename))
		return None
	try:
		imgbuffer = []
		im = Image.open(filename)
		#转换为灰度图
		'''
		模式“1”为二值图像，非黑即白。但是它每个像素用8个bit表示，0表示黑，255表示白。
		模式“L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
		在PIL中，从模式“RGB”转换为“L”模式是按照下面的公式转换的：
		L = R * 299/1000 + G * 587/1000+ B * 114/1000
		'''
		im = im.convert('L')
		(w, h) = im.size
		#将图片转换为160x160大小的点阵，如果图片大于或小于160x160，则进行resize操作
		print("img col={},row={}".format(im.size[0], im.size[1]))
		'''
		f = 0.00
		r = 0 
		if w != h:
			r = max(w, h)
			f = 160 / r 
		else:
			f = 160 / w 

		#是否改变图片的小大
		if fullscreen == True:
			#全屏幕显示
			if keepshape == True:
				im = im.resize((int(w * f), int(h * f)))
			else:
				im = im.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
		else:
			#原图大小显示
			if r > max(IMAGE_WIDTH, IMAGE_HEIGHT):
				print("show_image_on_screen image too big")
				return False
		#resize结束
		'''

		im.save("output.png")
		#获取图片每个点的像素值，根据需要如果需要
		(w, h) = im.size
		img = []
		for i in range(h):
			line = []
			for j in range(w):
				pv = im.getpixel((j, i))
				if pv < 180:
					line.append(0xf)
				else:
					line.append(0)
			if colreverse is True:
				line.reverse()
			img.append(line)
		if rowreverse is True:
			img.reverse()
		''' 
		如果图片缩小后不是160x160而是160x100或140x160
		那么就将对应的空白空间用0取代
		
		将图片的像素点放置在屏幕的中央
		'''
		left = int((IMAGE_WIDTH - w) / 2)
		top = int((IMAGE_HEIGHT - h) / 2)
		cur = 0 
		for row in range(IMAGE_HEIGHT):
			if row < top or row >= (IMAGE_HEIGHT - top):
				imgbuffer.append([0x0] * IMAGE_WIDTH)
			else:
				line = []
				line += [0x0] * left
				line += img[cur]
				line += [0x0] * left
				imgbuffer.append(line)
				cur += 1
		return imgbuffer
	except Exception as e:
		print("show_image_on_screen error:{}".format(e))
		return None

'''
将160x160的图片数据信息转换为160x81的数组，用来给160160点阵屏来显示
'''
def write_buffer_to_file(filename:str, imgbuffer:list):
	try:
		#检查目标文件是否存在，如果存在则删除掉它
		if os.path.exists(filename):
			os.remove(filename)

		playbuffer = []
		for i in range(81*160):
			playbuffer.append(0)

		i = 0
		for line in imgbuffer:
			j = 0
			pos = 0
			for point in line:
				if (j!=0) and (j%2==0):
					pos += 1
				if (j % 2 != 0):
					val = int(playbuffer[i * 81 + pos])
					val |= int(point)
					playbuffer[i * 81 + pos] = val
				else:
					val = int(playbuffer[i * 81 + pos])
					val |= int(point << 4)
					playbuffer[i * 81 + pos] = val
				j += 1
			i += 1

		print("playbuffer len={}".format(len(playbuffer)))
		with open(filename, 'wb+') as f:
			#imagebuffer = " ,".join(str(val) for val in playbuffer)
			'''
			imagebuffer = ""
			pos = 0
			for val in playbuffer:
				if pos % 81 == 0 and pos != 0:
					imagebuffer = "{}{}".format(imagebuffer, "\n")
				if len(imagebuffer) == 0:
					imagebuffer = "{}".format(str(val))
				else:
					imagebuffer = "{},{}".format(imagebuffer, str(val))
				pos += 1
			result = "{}{}{}".format("uint8_t imgbuf[] = {\n", imagebuffer, "\n};")
			f.write(result)
			'''
			f.write(bytes(playbuffer))
	except Exception as e:
		print("write_buffer_to_file error {}".format(e))

if __name__ == "__main__":
	fname = sys.argv[1]
	tarfilename = sys.argv[2]
	#生成直接放在设备上显示的图像数据
	img = show_image_on_screen(fname, True, True, rowreverse=True, colreverse=False)
	#生成利于人眼观察的图像，通过工具修改后在用脚本调转角度
	#img = show_image_on_screen(fname, True, True, rowreverse=False, colreverse=False)
	if img is not None:
		write_buffer_to_file(tarfilename, img)

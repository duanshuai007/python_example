# 将图片转换为点阵，用于点阵屏幕的显示

- step1: 通过imageto160x81martix.py脚本获取图像点阵信息文件

`python4 imageto160x81martix.py cc50e3957a6e.png image.dat`

- step2:利用notepad或者其他能够编辑binary文件的工具对点阵图进行修改

- step3:最后利用change_image_data_updownreverse.py脚本将图像反转为我们需要的图像。


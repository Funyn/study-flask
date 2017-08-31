#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-27 18:12:37
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from PIL import Image


#创建Image实例 
imagefile = os.path.join(os.getcwd(),'qiyu.jpg')    #path.join 将里面的内容用\链接,相当于list的join,不是字符串拼接
path = os.path.splitext(imagefile)  #splitext可以分解成 路径和扩展名 ('C:\\Users\\Administrator\\Desktop\\qiyu', '.jpg')
im = Image.open(imagefile)   #实例一个Image对象,从文件中加载图片         文件找不到会有一个FileNotFoundError
print(im.format,im.size,im.mode)     #im.format 标识图像来源			文件打开错误会有一个IOError
									#im.size 图片的（width，height)
									# im.mode 图片的模式   'L' ,'RGB' ,'CMYK'
# im.save('testfile/qiyulaoshi.jpg')  	#保存时候的必要参数  '路径+文件名+图片格式' 可以是相对于脚本的路径,也可以是绝对路径

#Im对象的方法
# im.show() #显示图片
#--------------------创建缩略图------------------------
# im.thumbnail((128,128),Image.ANTIALIAS)
# im.show()
# im.save('C:\\Users\\Administrator\\Desktop\\qiyu.thumbnail.jpeg')
#--------------------剪切(crop),转动图片(transpose),粘贴(paste)-----------------
#crop的参数是一个(左,上,右,下)的4元矩阵元组,大小是  width = 右减去左, height = 下减去上 返回一个新的im图片对象,不过是被剪切过后的
cr_im = im.crop((50,50,300,300))
# cr_im.show()
#transpose转动Image.ROTATE_180  转动180度 返回一个新的对象
tr_im = cr_im.transpose(Image.ROTATE_180)  
# tr_im.show()
#paste粘贴 第一个参数是 粘贴对象,4元矩阵
im.paste(cr_im)    
r,g,b = im.split() 	#单通道的图片分离后会是自己本身,对象的split()方法
print(r.__dict__,g,b)   #__dict__查看对象的内的属性与对应的值
im = Image.merge('RGB',(r,g,b))  #合并颜色通道Image.merge('im.mode',(r,g,b))
# im.show()





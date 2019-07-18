import os
import numpy as np
import pandas as pd
import binascii
from collections import defaultdict

def getImg(filename):
	with open(filename,'rb') as f:
        # f.seek(startindex, 0)
		content = f.read()
	hex_str = binascii.hexlify(content) # 将二进制文件转为十六进制字符串
	byte_array = np.array([int(hex_str[i:i+2],16) for i in range(0, len(hex_str), 2)])  # 按字节分割
	byte_array = np.uint8(byte_array) # 转成0-255的数字
	# print(byte_array[0:300])
	return byte_array

basepath = "../input/"
mapimg = defaultdict(list)
trainLabels = pd.read_csv('../input/trainLabels.csv')
print ('Loaded',len(trainLabels),'rows of trainLabels')
i = 0
for sid in trainLabels.Id:
	i += 1
	if i%100==0:
	    print("dealing with {0}th file...".format(str(i)))
	filename = basepath + sid + ".asm"
	img = getImg(filename)
	mapimg[sid] = img

dataframe_list = []
for sid,img in mapimg.iteritmes():
	tmp = {}
	tmp["Id"] = sid
	for index,value in enumerate():
		colName = "pix{0}".format(str(index))
		tmp[colName] = value
	dataframe_list.append(tmp)

df = pd.DateFrame(dataframelist)
df.to_csv("img_feature.csv")

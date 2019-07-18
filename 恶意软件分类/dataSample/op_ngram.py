import re
from collections import *
import os
import pandas as pd

def getOpSeq(filename): # 获取指令序列
	op_seq = []
	pattern = re.compile(r'\s([a-fA-F0-9]{2}\s)+\s*([a-z]+)')
	with open(filename) as f:
		for line in f:
			if line.startswith(".text"):
				m = re.findall(pattern,line) # 返回line中所有与p相匹配的全部字串，返回形式为数组
				if m:
					op = m[0][1] # ?
					if op != "align":
						op_seq.append(op)

	return opcode_seq

def getOpNgram(op_seq,n=4): # 统计指令序列的ngram
	op_ngram_list = [tuple(op_seq[i:i+n]) for i in range(len(ops)-n)]
	op_ngram = Counter(op_ngram_list) # 记数函数
	return op_ngram # opcode ngrams及对应出现次数

basepath = "../input/"
map_4gram = defaultdict(list)
trainLabels = pd.read_csv('../input/trainLabels.csv') 
print ('Loaded',len(trainLabels),'rows of trainLabels')
i = 0
for sid in trainLabels.Id:
	i += 1
	if i%100==0:
	    print("counting opcode 4gram of {0}th file...".format(str(i)))
	filename = basepath + sid + ".asm"
	op_seq = getOpSeq(filename)
	op_ngram = getOpNgram(op_seq)
	map_4gram[sid] = op_ngram

# 关注在所有asm文件中总共出现了500次以上的opcode
counter = Counter([])
for op in map_4gram.values():
	counter += op
selected = {}
for op,cnt in counter.iteritems():
	if cnt >= 500:
		selected[op] = cnt
		print(op,cnt)

dateframelist = []
for sid,op_ngram in map_4gram.iteritems():
	tmp = {}
	tmp["Id"] = sid
	for feature in selected:
		if feature in op_ngram:
			tmp[feature] = op_ngram[feature]
		else:
			tmp[feature] = 0
	dateframelist.append(tmp)
df = pd.DataFrame(dateframelist)
df.to_csv("op_4gram_features.csv",index=False)


# file = "0A32eTdBKayjCWhZqDOQ.asm"
# ops = getOpSeq(file)
# opngram = getOpNgram(ops)
# print(opngram)


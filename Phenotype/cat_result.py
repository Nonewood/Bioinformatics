# 接上一个差异检验的脚本 cat_diff.R ，处理其结果，整理成发表文章用的格式，略加改动就可以；

import os
group = ['NS','FS','CS'] # 组名

with open('diff_results.xls', 'r') as IN, open('Final_result.xls','w') as out:
	head = IN.readline().strip('\n').split('\t')
	print('\t'.join([head[0], '\t'.join(group), head[1]]), file = out)
	for line in IN:
		line = line.strip('\n').split('\t')
		outline = '\t'.join([line[0] + ',n(%)', '\t'*len(group)]) 
		print(outline + '%.2e' % float(line[1]), file = out) #格式化输出，科学计数法，保留两位小数点... 
		with open(line[0] + '_information.xls', 'r') as indice:
			indice.readline()
			for line in indice:
				line = line.strip('\n')
				print(line, file = out)
	#	os.remove(line[0] + '_information.xls')

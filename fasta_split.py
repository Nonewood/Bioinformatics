#按照 fasta 的 ID 和序列切分 fasta 文件，按 ID 输出想要的 fasta 序列（注释掉）
#! /usr/bin/python3
import os,sys
## write the fasta file into directory
#otu_ID = sys.argv[1]
inputFile = sys.argv[1]  # fasta 文件
basename = os.path.basename(inputFile)
outFile = 'filter_' + basename
fasta_dict = dict()
with open (inputFile, 'r') as IN:
	seq = ''
	key = ''
	for line in IN:
		if line.startswith('>'):
			fasta_dict[key] = seq
			key = line
			seq = ''
		else:
			seq = seq + line

	fasta_dict[key] = seq

del fasta_dict['']

##按照键值对输出 fasta 的序列，可以自己拿个小文件测试
for key in fasta_dict:
	print (key + '==>' + fasta_dict[key]) 

'''
#process otu ID file
with open(otu_ID, 'r') as IN, open(outFile, 'w') as out:
	for line in IN:
		ID = '>' + line
		if ID in fasta_dict:
			out.write(ID + fasta_dict[ID])

'''

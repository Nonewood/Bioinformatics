#! /usr/bin/python3
# 根据 OTU ID 提取 fasta 序列， eg: python3 otu_fasta.py ../Temp/otuID ../Temp/otu_demo.fasta 
import os,sys
## write the fasta file into directory
otu_ID = sys.argv[1]
inputFile = sys.argv[2]
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

#process otu ID file
with open(otu_ID, 'r') as IN, open(outFile, 'w') as out:
	for line in IN:
		ID = '>' + line
		if ID in fasta_dict:
			out.write(ID + fasta_dict[ID])

'''
for key in fasta_dict:
	print (key + '==>' + fasta_dict[key])
'''

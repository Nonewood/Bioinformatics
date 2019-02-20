#! /usr/bin/python3
# calculate the frequency of occurence of ciations in an article
import re
quotation = dict()
with open('quotation.txt', 'r') as IN:
	for line in IN:
		line = line.strip('\n')
		match = re.search('(\d+)\. (.*)', line)
		if match:
			number = match.group(1)
			article_name = match.group(2)	
			quotation[int(number)] = article_name

from collections import defaultdict
counts = defaultdict(int) #values will initialize to 0
with open('content.txt', 'r') as IN:
	for line in IN:
		match = re.findall('\[(\d+)\]',line)
		if match:
			for x in match:
				counts[int(x)] += 1 
with open('results.txt', 'w') as out:
	print('citation_number\tfrequency of occurrence\tarticle_title', file = out)
	for key in sorted(counts.keys()):
		print(str(key) + '\t' + str(counts[key]) + '\t' + quotation[key], file = out)


#! /usr/bin/python3
# 计算 beta 多样性
import argparse,re,os,math
import pandas as pd
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Generate the bray-curtis distance matrix based on abundance file.
Example: python3 braycurtis.py -i GeneCatalog_profile.xls.gz
To be continued.
------------------'''
)
parser.add_argument('-i','--Input', help = "the abundance file.")
parser.add_argument('-o','--outdir',help = "the output directory,default is current working directory.",nargs='?')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args=parser.parse_args()
abdfile = args.Input
outdir = args.outdir if args.outdir else './'
if not os.path.exists(outdir):
	os.makedirs(outdir)
out = outdir + '/braycurtis.txt'

if not abdfile:
	parser.print_help()
	exit()

if abdfile.endswith('gz'):
	df = pd.read_csv(abdfile, compression='gzip', header=0, sep='\t')
else:
	df = pd.read_csv(abdfile, header=0, sep='\t')

from scipy.spatial import distance
import pandas as pd
dt = pd.read_table(abdfile, index_col=0)
#dt.index = dt['geneID']
#dt.drop(['geneID'], axis=1, inplace=True) #好奇怪，我为什么要加这两行... 已然忘记了..
with open(out, 'w') as bray:
	print('\t' + '\t'.join(dt.columns.values), file = bray)
	for first in dt.columns.values:
		lst = list()
		lst.append(first)
		for second in dt.columns.values:
			dis = distance.braycurtis(dt[first], dt[second])
			lst.append(str(dis))
		print('\t'.join(lst), file=bray)

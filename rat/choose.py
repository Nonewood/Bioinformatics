#! /usr/bin/python3
import pandas as pd
import argparse,os,re
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
choose columns of the file by characters in rownames or colnames
Example: /ifshk7/BC_PS/wangpeng7/Software/Python-3.6.4/Build/bin/python3 split.py -i expose_genusProfileTable.xls -g Sample_information_detail.txt -s Cig-F:EL-F -o ./ 
To be continued.
------------------'''
)
parser.add_argument('-i','--Input', help = "the abundance file.", nargs='?') 
parser.add_argument('-g','--group', help = "the group file.", nargs='?')
parser.add_argument('-s','--splitID', help = "the character for spliting.")
parser.add_argument('-o','--outdir',help = "the output directory,default is current working directory.",nargs='?')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args=parser.parse_args()
abdfile = args.Input
groupfile = args.group
splitlist = args.splitID
optionpar = [abdfile,groupfile]
if not any(optionpar):
	print('\nError:you need add abundance or group file!\n')
	parser.print_help()
	exit()
if not splitlist:
	print('\nError:you need add split character!\n')
	parser.print_help()
	exit()
outdir = args.outdir if args.outdir else '.'

if abdfile:
	name = os.path.basename(abdfile)
#	dt = pd.read_table(abdfile, header=0, index_col=0)
	dt = pd.read_table(abdfile, header=0)
	dt.set_index(dt.columns[0], inplace=True) # for gene profile
	lst = splitlist.split(':') #two element 
	if len(lst) > 1:
		match = re.search('.*-(.*)',lst[0])
		outfile = outdir + '/' + match.group(1) + '_' + name
		with open(outfile,'w') as out:
			dt_temp = dt.loc[:,dt.columns.str.contains(lst[0])|dt.columns.str.contains(lst[1])]
			dt_temp = dt_temp.loc[(dt_temp != 0).sum(axis=1) != 0,:]
			dt_temp.to_csv(outfile, sep='\t')
	else:
		expose_dt = dt.loc[:,dt.columns.str.contains('-a') == False] #暂且写成这样..
		recovery_dt = dt.loc[:,dt.columns.str.contains('-a')]
		expose_dt.to_csv('expose_'+name, sep='\t')
		recovery_dt.to_csv('recovery_'+name, sep='\t')		

if groupfile:
	name = os.path.basename(groupfile)
	group = pd.read_table(groupfile, header=0, index_col=0)
	lst = splitlist.split(':')
	outfile = outdir + '/' + match.group(1) + '_' + name
	with open(outfile,'w') as out:
		group_temp = group.loc[group.index.str.contains(lst[0])|group.index.str.contains(lst[1]),:]
		group_temp.to_csv(outfile, sep='\t')

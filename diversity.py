#! /usr/bin/python3
import argparse,re,os,math
import pandas as pd
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Calculate the diversity index based on abundance file with pandas, only include number and shannon so far.
Example: python3 diversity.py -i GeneCatalog_profile.xls.gz
To be continued.
mood:feel happy to do things, do not need to think sad things.
------------------'''
)
parser.add_argument('-i','--Input', help = "the abundance file.")
parser.add_argument('-o','--outdir',help = "the output directory,default is current working directory.",nargs='?')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args=parser.parse_args()
abdfile = args.Input
outdir = args.outdir if args.outdir else './'
out = outdir + '/diversity.txt'

if abdfile.endswith('gz'):
	df = pd.read_csv(abdfile, compression='gzip', header=0, sep='\t')
else:
	df = pd.read_csv(abdfile, header=0, sep='\t')

df.columns.values[0] = 'geneID'
df = df.set_index('geneID')
sampleNumber = (df!=0).sum(axis=1)
indexSelect = sampleNumber.index[sampleNumber >= 81*0.1]
dfSelect = df.loc[indexSelect]
dfSelectSum = dfSelect.div(dfSelect.sum(axis=0), axis=1)
dt = dfSelectSum
geneNumber = (dt!=0).sum(axis=0)
shannon = dt.apply(lambda x: [-math.log(y)*y if y > 0 else 0 for y in x]).sum()
diversity = pd.concat([geneNumber, shannon], axis=1, keys=['number','shannon'])
diversity.to_csv(out, sep='\t')

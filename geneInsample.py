#得到基因丰度表以后，计算基因在样本中的存在情况，如至少在 10% 的样本存在的基因有多少，20%，30%... 以此类推, 并且按照需要输出低于某一阈值的基因 ID, 用来后续分析的过滤，如在少于 10% 样品中存在的基因 ID.

#！/usr/bin/python3
import pandas as pd
import argparse
import pandas as pd
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Calculate the the number of genes beyond some threshold(eg:exist in 10%, 20%.. of all sample)
Example: python3 geneInsample.py -i GeneCatalog_profile.xls.gz
abundance file > 5G needs vf > 20G.
To be continued.
------------------'''
)
parser.add_argument('-i','--Input', help = "the abundance file.")
parser.add_argument('-o','--outdir',help = "the output directory,default is current working directory.",nargs='?')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args=parser.parse_args()
abdfile = args.Input
outdir = args.outdir if args.outdir else '.'
outpath = outdir + '/geneInsample.txt'

if abdfile.endswith('gz'):
    df = pd.read_csv(abdfile, compression='gzip', header=0, sep='\t')
else:
    df = pd.read_csv(abdfile, header=0, sep='\t')

df.columns.values[0] = 'geneID'
df = df.set_index('geneID')
totalsample = len(df.columns)
sampleNum = (df!=0).sum(axis=1)
totalGene = len(sampleNum)

gene_10 = sampleNum[sampleNum >= totalsample*0.1]
per_10 = len(gene_10)
#print out the genes exist more than in 10% samples
with open('GeneOfTen.txt','w') as gene:
    gene_10.to_csv(gene, sep='\t')
per_10_rate = round(per_10/totalGene,2)

per_20 = len(sampleNum[sampleNum >= totalsample*0.2])
per_20_rate = round(per_20/totalGene,2)
per_30 = len(sampleNum[sampleNum >= totalsample*0.3])
per_30_rate = round(per_30/totalGene,2)
per_40 = len(sampleNum[sampleNum >= totalsample*0.4])
per_40_rate = round(per_40/totalGene,2)
per_50 = len(sampleNum[sampleNum >= totalsample*0.5])
per_50_rate = round(per_50/totalGene,2)
per_60 = len(sampleNum[sampleNum >= totalsample*0.6])
per_60_rate = round(per_60/totalGene,2)
per_70 = len(sampleNum[sampleNum >= totalsample*0.7])
per_70_rate = round(per_70/totalGene,2)
per_80 = len(sampleNum[sampleNum >= totalsample*0.8])
per_80_rate = round(per_80/totalGene,2)
per_90 = len(sampleNum[sampleNum >= totalsample*0.9])
per_90_rate = round(per_90/totalGene,2)
with open (outpath,'w') as out:
    out.write('\t'.join(['threshold','number','rate']) + '\n')
    out.write('\t'.join(['>=0', str(totalGene), '1']) + '\n')
    out.write('\t'.join(['>=10%', str(per_10), str(per_10_rate)]) + '\n')
    out.write('\t'.join(['>=20%', str(per_20), str(per_20_rate)]) + '\n')
    out.write('\t'.join(['>=30%', str(per_30), str(per_30_rate)]) + '\n')
    out.write('\t'.join(['>=40%', str(per_40), str(per_40_rate)]) + '\n')
    out.write('\t'.join(['>=50%', str(per_50), str(per_50_rate)]) + '\n')
    out.write('\t'.join(['>=60%', str(per_60), str(per_60_rate)]) + '\n')
    out.write('\t'.join(['>=70%', str(per_70), str(per_70_rate)]) + '\n')
    out.write('\t'.join(['>=80%', str(per_80), str(per_80_rate)]) + '\n')
    out.write('\t'.join(['>=90%', str(per_90), str(per_90_rate)]) + '\n')
 

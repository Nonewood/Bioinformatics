#得到基因丰度表以后，计算基因在样本中的存在情况，如至少在 10% 的样本存在的基因有多少，20%，30%... 以此类推, 并且按照需要输出低于某一阈值的基因 ID, 用来后续分析的过滤，如在少于 10% 样品中存在的基因 ID.

#！/usr/bin/python3
import pandas as pd
import argparse
import matplotlib
matplotlib.use('Agg') # 不加这个画图的时候会报错

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
sampleNum = (df!=0).sum(axis=1)  # the sample numers of each gene, including genes exist in no samples
geneOf_0 = sum(sampleNum == 0)  # judge the genes number  exist in no samples
# error
if geneOf_0:
	print("some genes do not exist in all samples! please check your file!\nThe corresponding gene numbers is " + str(geneOf_0) + ' :)')
	#exit()
else:
	next

totalGene = sum(sampleNum != 0)

out = open (outpath,'w')
out.write('\t'.join(['threshold','sampleNumber','geneNumber','rate']) + '\n')
out.write('\t'.join(['>0', '1', str(totalGene), '1']) + '\n')
for x in range(10,91,10):
	threshold = '>=' + str(x) + '%'
	sampleNumber = int(totalsample*(x/100)) + 1
	geneNumber = len(sampleNum[sampleNum >= sampleNumber])
	geneRate =  round(geneNumber/totalGene,2)
	out.write('\t'.join([threshold,str(sampleNumber),str(geneNumber),str(geneRate)]) + '\n')
out.close()

### plot ###
import seaborn as sns
import matplotlib.pyplot as plt
dt = pd.read_table(outdir + '/geneInsample.txt', sep='\t', header=0)
sns.set_style("ticks")
p = sns.barplot(x=dt["sampleNumber"],y=dt["geneNumber"])
p.axes.set_title("geneINsample", size=14)
p.set_xlabel("sample numbers(>=)", size=12)
p.set_ylabel("gene numbers", size=12)
p.tick_params(labelsize=10)
fig = p.get_figure()
fig.savefig(outdir+ "geneINsample.pdf")

#print out the genes exist more than in 10% samples
'''
sampleOfTen = int(totalsample*0.1)
geneOfTen = sampleNum[sampleNum >= sampleOfTen]
with open('GeneOfTen.txt','w') as gene:
	geneOfTen.to_csv(gene, sep='\t')
geneprofile_10 = df[sampleNum >= sampleOfTen]
with open('geneprofile_10','w') as profile:
    geneprofile_10.to_csv(profile, sep='\t')
'''

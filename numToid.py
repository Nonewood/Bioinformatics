#过滤出来至少在 10% 样品中存在的基因编号后，需要得到相应的基因 ID (因为之前基因长度文件配置的缘故，现在要替换回来).没有用字典，试着用 pandas 的 concat 功能, 将两个数据集按照行索引取交集合并，提取编号和与之对应的 ID, 单独输出到文件.
#主要是想多试试用 pandas.

#! /usr/bin/python3
import pandas as pd
df = pd.read_table('tempNon-redundant_Gene_Catalog_length_gc.xls.gz', compression='gzip', header=0, index_col=0)
dt = pd.read_table('GeneOfTen.txt', header=None, names=['geneNum','sampleNum'], index_col=0)
merge = pd.concat([df,dt], axis=1, join='inner')
numToid = merge['Name']
numToid.to_csv('numToid.txt', sep='\t')


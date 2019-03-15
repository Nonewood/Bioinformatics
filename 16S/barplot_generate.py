#! /usr/bin/python3
###############################
#根据丰度表或者其他进行归一化，然后提取指定的一组物种或者 OTU, 并且生成带有分组信息的 barplot.txt 用于绘制 barplot, 最后生成物种或者 OTU 的排序；   
#时间关系，就不写成加外参的形式了，需要的文件在 Data 文件夹下边；
#关键词：归一；排序；
###############################
import pandas as pd
#转化为相对丰度，并且提取需要的 OTU 的丰度
dt = pd.read_table('OTU_table_for_biom.txt', header = 1, index_col = 0)
dt = dt.iloc[:,:-1] #筛选列
dt = dt.div(dt.sum(axis=0), axis=1) # 这一招绝了...佩服以前的自己


with open('otu_id.txt', 'r') as IN:
    otu_list= IN.read().split('\n')
    otu_list.remove('')
df = dt.loc[otu_list]
df.to_csv('filter_OTU_table.txt', sep = "\t")

# 提取样品分组信息
group_dict = dict()
group_dt = pd.read_table('bms.info', index_col = 0)
#group_dt.head()
for item in group_dt.index:
    group_dict[item] = group_dt.loc[item]['Description']
    
#生成画 barplot 的图，四列，没有考虑合并低丰度的问题，也没过滤某个样本所有 OTU 都为零的情况；
from collections import defaultdict
with open('filter_OTU_table.txt', "r") as IN, open('barplot.txt', "w") as out:
    out.write('individual\ttax\tabundance\tgroup\n')
    head = IN.readline().strip('\n').split('\t')
    Dict = defaultdict(float)
    for line in IN:
        lst = line.strip('\n').split('\t')
        taxonomy = lst[0]
        for index in range(1,len(lst)):
            key = head[index] + "\t" + taxonomy + "\t" + lst[index]
            Dict[key] = head[index]
    for key in Dict:
        keys = key.split('\t')
        indiv = keys[0]
        taxonomy = keys[1]
        abund = keys[2]
        out.write(indiv + '\t' + taxonomy + '\t' + abund + '\t' + group_dict[indiv] + '\n')      

#tax_order 图例的顺序，这里是 OTU 的顺序，按照全部样品中的 OTU 的均值排列     
dt = pd.read_table('barplot.txt', index_col=0)
tax_order = list(dt.groupby('tax').abundance.mean().sort_values(ascending=False).index)
tax_order = ','.join(['"' + x + '"' for x in tax_order])    

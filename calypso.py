# 将物种丰度表处理成 Calyps 软件能够接受的输入文件
import pandas as pd
dt = pd.read_table('phylumProfileTable.xls')
Phylum = pd.Series(['phylum'] * len(dt.index.values)) #生成和行数相同的 phylum 
dt = pd.concat([Phylum,dt], axis=1) # 合并，横向合并
dt.columns.values[0] = 'Phylum' 
dt.columns.values[1] = 'Header'  #对列名进行重命名
dt.to_csv('Calypso_phylum.txt', sep='\t', index=False) #输出，并且关闭输出掉索引值


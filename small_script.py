#! /usr/bin/python3 
import pandas as pd
from numpy import nan

df = pd.read_table('genome.list.filter.anno')
tax = df['Taxonomy'].str.split(';', expand=True) # 按照分号将 'Taxonomy' 分割，并且储存成数据库格式
tax.fillna(value=nan, inplace=True) # 将 None 替换为 Nan
it2level= tax.count(axis=1) #按照列求和 
id2level.unique() # unique 功能
(id2level == 2).sum()
(id2level == 6).sum()
(id2level == 7).sum() # 统计门，属，种水平的基因数目


## 在同事差异物种脚本的基础上，为箱线图生成显著性的标识 **/* 等，只适用于三组的两两标识；其他组别待开发；
## 属水平
group = ['NS', 'FS', 'CS'] # 要和下边的差异文件对应， g1,g2,g3

g1_g2 = pd.read_table('genus.FS-NS.wilcox.test.xls', index_col = 0)
g2_g3 = pd.read_table('genus.CS-FS.wilcox.test.xls', index_col = 0)
g1_g3 = pd.read_table('genus.CS-NS.wilcox.test.xls', index_col = 0)

## 同事画图文件
dt = pd.read_table("genus.relab_profile.xls", index_col = 0)
#dt = dt.drop(['Others'], axis = 1)
tax = list(dt.columns[1:]) # 不要 group
#tax.remove('Others')

dt_max = dt.groupby('Group').max() # 取得最大值
#import numpy as np

## g1 and g2 
g1_g2_max = dt_max.loc[[group[0], group[1]]].max() + 0.2 # 获得两两分组物种的最大值
g1_g2_order = g1_g2.loc[tax]
g1_g2_order['lab'] = g1_g2_order.apply(lambda x: '***' if x.qvalue < 0.001 else ( '**' if x.qvalue < 0.01 else ('*' if x.qvalue < 0.05 else 'NA')), axis =1)
x2 = [tax.index(item) + 1 for item in tax]  # 左坐标
x1 = [item - 0.3 for item in x2] #右坐标
xstar = [item - 0.15 for item in x2] # ** 位置
g1_g2_order['x1'] = x1
g1_g2_order['x2'] = x2
g1_g2_order['xstar'] = xstar
g1_g2_order['y1'] = g1_g2_max.loc[tax]
g1_g2_order['y2'] = g1_g2_max.loc[tax] + 0.1
g1_g2_order['ystar'] = g1_g2_max.loc[tax] + 0.2
g1_g2_sig = g1_g2_order.loc[g1_g2_order['lab'] != 'NA'].loc[:,['x1', 'x2', 'xstar', 'y1', 'y2', 'ystar', 'lab']]
g1_g2_sig

## g1 and g3 
g1_g3_max = dt_max.loc[[group[0], group[2]]].max() + 0.2 # 或者两两分组物种的最大值
g1_g3_order = g1_g3.loc[tax]
g1_g3_order['lab'] = g1_g3_order.apply(lambda x: '***' if x.qvalue < 0.001 else ( '**' if x.qvalue < 0.01 else ('*' if x.qvalue < 0.05 else 'NA')), axis =1)
x1 = [tax.index(item) + 1 - 0.3 for item in tax] 
x2 = [item + 0.6 for item in x1]
xstar = [item - 0.3 for item in x2]
g1_g3_order['x1'] = x1
g1_g3_order['x2'] = x2
g1_g3_order['xstar'] = xstar
g1_g3_order['y1'] = g1_g3_max.loc[tax] 
g1_g3_order['y2'] = g1_g3_max.loc[tax] + 0.1
g1_g3_order['ystar'] = g1_g3_max.loc[tax] + 0.2
g1_g3_sig = g1_g3_order.loc[g1_g3_order['lab'] != 'NA'].loc[:,['x1', 'x2', 'xstar', 'y1', 'y2', 'ystar', 'lab']]
g1_g3_sig


## g2 and g3 
g2_g3_max = dt_max.loc[[group[1], group[2]]].max() + 0.2 # 或者两两分组物种的最大值
g2_g3_order = g2_g3.loc[tax]
g2_g3_order['lab'] = g2_g3_order.apply(lambda x: '***' if x.qvalue < 0.001 else ( '**' if x.qvalue < 0.01 else ('*' if x.qvalue < 0.05 else 'NA')), axis =1)
x1 = [tax.index(item) + 1 for item in tax] 
x2 = [item + 0.3 for item in x1]
xstar = [item - 0.15 for item in x2]
g2_g3_order['x1'] = x1
g2_g3_order['x2'] = x2
g2_g3_order['xstar'] = xstar
g2_g3_order['y1'] = g2_g3_max.loc[tax]
g2_g3_order['y2'] = g2_g3_max.loc[tax] + 0.1
g2_g3_order['ystar'] = g2_g3_max.loc[tax] + 0.2
g2_g3_sig = g2_g3_order.loc[g2_g3_order['lab'] != 'NA'].loc[:,['x1', 'x2', 'xstar', 'y1', 'y2', 'ystar', 'lab']]
g2_g3_sig

all_dt = pd.concat([g1_g2_sig,g1_g3_sig, g2_g3_sig])
all_dt.to_csv('genus_plabel.txt', sep = '\t')

#用于生成使用 humann2_barplot 画 barplot 的文件
import pandas as pd
dt = pd.read_table(pathabd_rename.xls', index_col = 0)
group = pd.read_table('phenotype.xls', index_col=0)
group_dt = group['Group'].to_frame('Group')
dt_merge = pd.concat([group_dt,dt.T], axis = 1)
dt_merge.T.to_csv('pathabd.pcl',sep = '\t')

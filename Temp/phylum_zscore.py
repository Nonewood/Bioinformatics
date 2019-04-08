# 计算蔡军 门 水平的 Zscore
## 计算 z core
dt = pd.read_table('/Users/tongxueer/Documents/20190214-北京/fuwai/CJ_phylum_abd.txt', index_col=0)
dt = dt.drop(['Tax_detail'], axis=1)
group = pd.read_table('/Users/tongxueer/Documents/20190214-北京/fuwai/CJ_phylum_map.txt', index_col=0)
from scipy.stats import zscore
dt_z = dt.apply(zscore, axis=1).T  ## 这行是用来计算 zscore
Control_mean = dt_z.loc[group.loc[group['Description'] == 'Control'].index].mean().to_frame(name='Control')
CHD_mean = dt_z.loc[group.loc[group['Description'] == 'CHD'].index].mean().to_frame(name='CHD')
STEMI_mean = dt_z.loc[group.loc[group['Description'] == 'STEMI'].index].mean().to_frame(name='STEMI')
z_merge = pd.concat([Control_mean,CHD_mean,STEMI_mean], axis=1)

# 提取差异物种 ID
Control_CHD = pd.read_table('/Users/tongxueer/Documents/20190214-北京/fuwai/Phylum.Control-CHD.wilcox.test.xls', index_col=0)
STEMI_Control = pd.read_table('/Users/tongxueer/Documents/20190214-北京/fuwai/Phylum.STEMI-Control.wilcox.test.xls', index_col=0)
STEMI_CHD = pd.read_table('/Users/tongxueer/Documents/20190214-北京/fuwai/Phylum.STEMI-CHD.wilcox.test.xls', index_col=0)

Control_CHD_diff = list(Control_CHD.loc[Control_CHD['qvalue'] < 0.05].index)
STEMI_Control_diff = list(STEMI_Control.loc[STEMI_Control['qvalue'] < 0.05].index)
STEMI_CHD_diff = list(STEMI_CHD.loc[STEMI_CHD['qvalue'] < 0.05].index)
diff_tax = Control_CHD_diff + STEMI_Control_diff  + STEMI_CHD_diff
diff_tax = list(set(diff_tax)) # 去重复
z_plot =  z_merge.loc[diff_tax].T
z_plot.to_csv('CJ_zscore_phylum.txt', sep="\t")

#注释的表格
temp = STEMI_Control.loc[STEMI_Control['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'p_png' if x < 0.01 else 'lessp_png'  for x in temp['qvalue']]
temp['Control vs STEMI'] = label
STEMI_Control_p = temp.drop(['qvalue'], axis=1)

temp = Control_CHD.loc[Control_CHD['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'p_png' if x < 0.01 else 'lessp_png'  for x in temp['qvalue']]
temp['Control vs CHD'] = label
Control_CHD_p = temp.drop(['qvalue'], axis=1)

temp = STEMI_CHD.loc[STEMI_CHD['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'p_png' if x < 0.01 else 'lessp_png'  for x in temp['qvalue']]
temp['CHD vs STEMI'] = label
STEMI_CHD_p = temp.drop(['qvalue'], axis=1)

all_p = pd.concat([STEMI_Control_p,Control_CHD_p,STEMI_CHD_p], axis=1)
all_p.fillna('no_sig_png').to_csv('CJ_phylum_annotation_col.txt', sep='\t')

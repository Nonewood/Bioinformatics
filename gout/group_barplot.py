
import pandas as pd
dt = pd.read_table("Gout_10gene_phylum_abundance_profile.xls", header = 0, index_col=0)
group = pd.read_table("Sample_information_detail_drug_20180806.xls", header = 0, index_col=0)

#dt_melt.columns.values[0] = 'Tax'
# 得到丰度前五的物种，将剩下的合并
dt_melt = pd.melt(dt.reset_index(), id_vars='index', value_vars = list(dt.columns)[0:], var_name = 'SampleID', value_name = 'Abundance') 
tax_mean = dt_melt.groupby('index').mean().sort_values(by = 'Abundance', ascending = False)
tax_retain = list(tax_mean.index[:5])
tax_others = list(tax_mean.index[5:])
dt_retain = dt.loc[tax_retain]
dt_others = dt.loc[tax_others].sum().to_frame(name = 'Others').T
dt_merge = pd.concat([dt_retain, dt_others])

## 根据合并后的丰度表，生成画 barplot 的柱状图文件
#ha = pd.melt(temp, id_vars = ['Description'], value_vars = list(temp.columns)[:-1], var_name = '', value_name = 'Abundance') 
# id_vars  表示不变的列名， value_vars 表示置换的列名，var_name 变化后的列名，这里是组名， value_name 是变化后的数值列名
dt_merge_melt = pd.melt(dt_merge.reset_index(), id_vars='index', value_vars = list(dt_merge.columns)[0:], var_name = 'SampleID', value_name = 'Abundance') 
dt_merge_melt.columns.values[0] = 'Tax'# 这里有雷，melt 以后重命名，在更改列名，会出现无法调用的情况，待定
#dt_merge_melt

#获取分组名
sample_group = group['SamplingTime'].to_frame().reset_index()
sample_group.columns.values[0] = 'SampleID'
barplot_dt = pd.merge(dt_merge_melt, sample_group, left_on = 'SampleID', right_on = 'SampleID')
barplot_dt.to_csv('gout_phylum_barplot.txt', sep = '\t', index = 0)

# 得到画图的物种顺序
control = barplot_dt.loc[(barplot_dt['Tax'] == 'Bacteroidetes') & (barplot_dt['SamplingTime'] == 'Control')]
control_list = list(control.sort_values(by='Abundance')['SampleID'])

T0 = barplot_dt.loc[(barplot_dt['Tax'] == 'Bacteroidetes') & (barplot_dt['SamplingTime'] == 'T0')]
T0_list = list(T0.sort_values(by='Abundance')['SampleID'])

T1 = barplot_dt.loc[(barplot_dt['Tax'] == 'Bacteroidetes') & (barplot_dt['SamplingTime'] == 'T1')]
T1_list = list(T1.sort_values(by='Abundance')['SampleID'])

T2 = barplot_dt.loc[(barplot_dt['Tax'] == 'Bacteroidetes') & (barplot_dt['SamplingTime'] == 'T2')]
T2_list = list(T2.sort_values(by='Abundance')['SampleID'])

T3 = barplot_dt.loc[(barplot_dt['Tax'] == 'Bacteroidetes') & (barplot_dt['SamplingTime'] == 'T3')]
T3_list = list(T3.sort_values(by='Abundance')['SampleID'])

sample_order = control_list + T0_list + T1_list + T2_list + T3_list
tax_order = list(dt_merge.index)

# R 画图的输入参数
R_sample_order = ":".join(sample_order)
R_tax_order = ":".join(tax_order)
R_color_order = ':'.join(["#99c885", "#e5abeb", "#e5ffb3","#49e4f2"]) # 来源网站
with open ('out.sh', 'w') as out:
    print('Rscript gout_group_barplot.R -i gout_phylum_barplot.txt -t ' + R_tax_order + ' -s ' + R_sample_order  + ' -r  Control:T0:T1:T2:T3 -c ' + R_color_order + ' -p gout_phylum')

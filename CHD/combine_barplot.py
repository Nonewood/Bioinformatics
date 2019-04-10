#对于任一指定水平生成按照分组对物种丰度取均值的文件，用于画合并的 barpolot 图，同时输出了物种的顺序, 输入文件在 Data 目录下
abd = pd.read_table('CJ_phylum_abd.txt', index_col=0)
abd = abd.drop('Tax_detail', axis=1) #我们的文件需要注释掉这一行
group = pd.read_table('CJ_phylum_map.txt', index_col=0)
sample_group = group.to_dict()
groups = list(group['Description'].unique())
dt_list = list()
for item in groups:
    dt = abd[[x for x in abd.columns if sample_group['Description'][x] == item]].mean(axis=1).to_frame(name='Mean')
    large = dt.loc[dt['Mean'] > 0.01]
    small = dt.loc[dt['Mean'] <= 0.01]
    small_merge = small.sum().to_frame(name = 'Others').T
    dt_merge = pd.concat([large,small_merge])
    dt_merge['Group'] = item
    dt_list.append(dt_merge)
bar_dt = pd.concat(dt_list)
bar_dt['Tax'] = bar_dt.index
bar_dt = bar_dt[['Tax', 'Mean', 'Group']]
bar_dt.to_csv('test.txt', index=0, sep='\t')
tax_order = list(bar_dt.groupby('Tax').mean().sort_values(by = 'Mean', ascending = False).index)
with open('plot_tax_order', 'w') as out:
    print(tax_order, file=out)

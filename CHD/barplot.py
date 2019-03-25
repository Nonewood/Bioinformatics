# 感觉非常个性化。。。所以就先不整合了，放在这里记录.. 包括生成物种组成柱状图，热图还有箱线图，涉及门水平，中水平，以及单独五个物种。
## CHD
#种的 barplot
import pandas as pd
dt = pd.read_table('MetaPhlAn2_species.draw_barplot.txt', index_col = 0,sep='\t')
group = pd.read_table('Mapping.txt', index_col = 0, sep='\t')
merge = pd.concat([dt,group.loc[dt.index]], axis=1)
merge['individual'] = merge.index
new_merge = merge.loc[:,['individual', 'level', 'abundance', 'Description']]
new_merge.columns.values[1] = 'tax'
new_merge.columns.values[3] = 'group'
new_merge.to_csv('CHD_barplot.txt', index=0, sep='\t')

## 合并后的 barplot
dt = pd.read_table('Species.combine_relative_abundance.xls', index_col = 0, sep='\t')
tax_list = ["Faecalibacterium_prausnitzii","Escherichia_coli","Eubacterium_rectale","Subdoligranulum_unclassified","Ruminococcus_bromii","Bifidobacterium_adolescentis","Klebsiella_pneumoniae","Bifidobacterium_longum","Alistipes_putredinis","Bacteroides_vulgatus","Escherichia_unclassified","Bacteroides_uniformis"]
dt_13 = dt.loc[tax_list]
other = dt[[False if x in tax_list else True for x in dt.index]] 
other_row = other.sum().to_frame(name = "Others").T
merge = pd.concat([dt_13, other_row])
merge.to_csv('CHD_combine_barplot.txt',sep = '\t')

#重新整理输出 barplot.txt
dt = pd.read_table('CHD_combine_barplot.txt', sep='\t', index_col=0)
AMI = dt['AMI'].to_frame(name = 'abundance')
AMI['group'] = 'AMI'
sCAD = dt['sCAD'].to_frame(name = 'abundance')
sCAD['group'] = 'sCAD'
NCA = dt['NCA'].to_frame(name = 'abundance')
NCA['group'] = 'NCA'
merge = pd.concat([AMI, sCAD, NCA])
merge['tax'] = merge.index
merge = merge[['tax','abundance', 'group']]
merge.to_csv('CHD_new_combine_barplot.txt', index = 0, sep = '\t')

# 计算 门 水平的 Zscore
## 计算 z core
dt = pd.read_table('Phylum.rabun.xls', index_col=0)
from scipy.stats import zscore
dt_z = dt.apply(zscore, axis=1).T
NCA_mean = dt_z.loc[group.loc[group['Description'] == 'NCA'].index].mean().to_frame(name='NCA')
sCAD_mean = dt_z.loc[group.loc[group['Description'] == 'sCAD'].index].mean().to_frame(name='sCAD')
AMI_mean = dt_z.loc[group.loc[group['Description'] == 'AMI'].index].mean().to_frame(name='AMI')
z_merge = pd.concat([NCA_mean,sCAD_mean,AMI_mean], axis=1)

# 提取差异物种 ID
NCA_sCAD = pd.read_table('Phylum_MetaPhlAn2.NCA-sCAD.wilcox.test.xls', index_col=0)
NCA_AMI = pd.read_table('Phylum_MetaPhlAn2.NCA-AMI.wilcox.test.xls', index_col=0)
AMI_sCAD = pd.read_table('Phylum_MetaPhlAn2.AMI-sCAD.wilcox.test.xls', index_col=0)

NCA_sCAD_diff = list(NCA_sCAD.loc[NCA_sCAD['qvalue'] < 0.05].index)
NCA_AMI_diff = list(NCA_AMI.loc[NCA_AMI['qvalue'] < 0.05].index)
AMI_sCAD_diff = list(AMI_sCAD.loc[AMI_sCAD['qvalue'] < 0.05].index)
diff_tax = NCA_sCAD_diff + NCA_AMI_diff  + AMI_sCAD_diff
diff_tax = list(set(diff_tax)) # 去重复
z_plot =  z_merge.loc[diff_tax].T
z_plot.to_csv('zscore_phylum.txt', sep="\t")

#注释的表格
temp = NCA_AMI.loc[NCA_AMI['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'P<0.01' if x < 0.01 else 'P<0.05'  for x in temp['qvalue']]
temp['NCA vs AMI'] = label
NCA_AMI_p = temp.drop(['qvalue'], axis=1)

temp = NCA_sCAD.loc[NCA_sCAD['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'P<0.01' if x < 0.01 else 'P<0.05'  for x in temp['qvalue']]
temp['NCA vs sCAD'] = label
NCA_sCAD_p = temp.drop(['qvalue'], axis=1)

temp = AMI_sCAD.loc[AMI_sCAD['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'P<0.01' if x < 0.01 else 'P<0.05'  for x in temp['qvalue']]
temp['sCAD vs AMI'] = label
AMI_sCAD_p = temp.drop(['qvalue'], axis=1)

all_p = pd.concat([AMI_sCAD_p,NCA_AMI_p,NCA_sCAD_p], axis=1)
all_p.fillna('No.sig').to_csv('annotation_col.txt', sep='\t')

#计算种水平的 Zscore
dt = pd.read_table('Species.rabun.xls', index_col=0)
from scipy.stats import zscore
dt_z = dt.apply(zscore, axis=1).T
NCA_mean = dt_z.loc[group.loc[group['Description'] == 'NCA'].index].mean().to_frame(name='NCA')
sCAD_mean = dt_z.loc[group.loc[group['Description'] == 'sCAD'].index].mean().to_frame(name='sCAD')
AMI_mean = dt_z.loc[group.loc[group['Description'] == 'AMI'].index].mean().to_frame(name='AMI')
z_merge = pd.concat([NCA_mean,sCAD_mean,AMI_mean], axis=1)

# 提取差异物种 ID
NCA_sCAD = pd.read_table('Species_MetaPhlAn2.NCA-sCAD.wilcox.test.xls', index_col=0)
NCA_AMI = pd.read_table('Species_MetaPhlAn2.NCA-AMI.wilcox.test.xls', index_col=0)
AMI_sCAD = pd.read_table('Species_MetaPhlAn2.AMI-sCAD.wilcox.test.xls', index_col=0)

NCA_sCAD_diff = list(NCA_sCAD.loc[NCA_sCAD['qvalue'] < 0.05].index)
NCA_AMI_diff = list(NCA_AMI.loc[NCA_AMI['qvalue'] < 0.05].index)
AMI_sCAD_diff = list(AMI_sCAD.loc[AMI_sCAD['qvalue'] < 0.05].index)
diff_tax = NCA_sCAD_diff + NCA_AMI_diff  + AMI_sCAD_diff
diff_tax = list(set(diff_tax)) # 去重复
z_plot =  z_merge.loc[diff_tax].T
z_plot.to_csv('zscore_species.txt', sep="\t")

# 生成标签
temp = NCA_AMI.loc[NCA_AMI['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'P<0.01' if x < 0.01 else 'P<0.05'  for x in temp['qvalue']]
temp['NCA vs AMI'] = label
NCA_AMI_p = temp.drop(['qvalue'], axis=1)

temp = NCA_sCAD.loc[NCA_sCAD['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'P<0.01' if x < 0.01 else 'P<0.05'  for x in temp['qvalue']]
temp['NCA vs sCAD'] = label
NCA_sCAD_p = temp.drop(['qvalue'], axis=1)

temp = AMI_sCAD.loc[AMI_sCAD['qvalue'] < 0.05]['qvalue'].to_frame()
label = [ 'P<0.01' if x < 0.01 else 'P<0.05'  for x in temp['qvalue']]
temp['sCAD vs AMI'] = label
AMI_sCAD_p = temp.drop(['qvalue'], axis=1)

all_p = pd.concat([AMI_sCAD_p,NCA_AMI_p,NCA_sCAD_p], axis=1)
all_p.fillna('No.sig').to_csv('species_annotation_col.txt', sep='\t')

# 挑选出的五个物种
dt = pd.read_table('zscore_species.txt', index_col=0)
items = ["Lactobacillus_mucosae", "Lactobacillus_crispatus", "Atopobium_parvulum", "Alistipes_onderdonkii", "Pyramidobacter_piscolens"]
five_zscore = dt[items]
five_zscore.to_csv('zscore_five_species.txt',sep="\t")
anno = pd.read_table('species_annotation_col.txt', index_col=0)
anno.loc[items].to_csv('five_species_annotation_col.txt', sep='\t')

## 直接生成差异物种（患者和健康人）的箱线图，患者之间单独比吧...
## 门水平
diff = dict()
with open('Phylum_MetaPhlAn2.NCA-sCAD.wilcox.test.xls') as IN:
    IN.readline()
    for line in IN:
        line = line.strip('\n').split('\t')
        if float(line[11]) < 0.05:
            diff[line[0]] = line[9]
        else:
            continue

case_list = ['sCAD', 'AMI']
hc_list = ['NCA']

with open('Phylum_MetaPhlAn2.NCA-AMI.wilcox.test.xls') as IN:
    IN.readline()
    for line in IN:
        line = line.strip('\n').split('\t')
        if float(line[11]) < 0.05:
            if line[0] in diff:
                if diff[line[0]] in case_list and line[9] in case_list:
                    continue
                elif diff[line[0]] in hc_list and line[9] in hc_list:
                    continue
                else:
                    print(line)
                    del diff[line[0]]
            else:
                diff[line[0]] = line[9]
        else:
            continue

#print(diff)
case_tax = list()
hc_tax = list()            
    
for key in diff:
    if diff[key] in case_list:
        case_tax.append(key)
    else:
        hc_tax.append(key)

## 对患者和健康人每组的物种按照所有样本均值的大小排序，得到 R 画图的 x 轴的顺序
dt = pd.read_table('Phylum.rabun.xls', index_col=0)
case_order = list(dt.loc[case_tax].mean(axis=1).sort_values(ascending = False).index)
hc_order = list(dt.loc[hc_tax].mean(axis=1).sort_values(ascending = False).index)
all_order = case_order[:14] + hc_order
print(':'.join(all_order))

# 有时候需要个性化一下
#all_order = ["Verrucomicrobia","Synergistetes"]

# 根据到的物种 ID 从丰度表里提取数据并且生成画箱线图的数据
#dt = pd.read_table('Species.rabun.xls', index_col=0)
dt.loc[all_order].to_csv('diff_species_abd.txt', sep='\t')
group = pd.read_table('Mapping.txt', index_col=0)
group_dict = group.to_dict()
with open('diff_phylum_abd.txt', 'r') as abd, open('phylum_boxplot.txt', 'w') as out:
    print('ID\tAbd\tGroup', file=out)
    head = abd.readline().strip('\n').split('\t')
    for line in abd:
        line = line.strip('\n').split('\t')
        if line[0] in all_order:
            for index in range(1,len(line)):
                if float(line[index]) != 0:
                    print(line[0] + '\t'+ line[index] + '\t' + group_dict[group.columns.values[0]][head[index]], file=out)           
                else:
                    print(line[0] + '\t'+ "1e-06" + '\t' + group_dict[group.columns.values[0]][head[index]], file=out)            

### 种水平的处理
diff = dict()
with open('Species_MetaPhlAn2.NCA-sCAD.wilcox.test.xls') as IN:
    IN.readline()
    for line in IN:
        line = line.strip('\n').split('\t')
        if float(line[11]) < 0.05:
            diff[line[0]] = line[9]
        else:
            continue

case_list = ['sCAD', 'AMI']
hc_list = ['NCA']

with open('Species_MetaPhlAn2.NCA-AMI.wilcox.test.xls') as IN:
    IN.readline()
    for line in IN:
        line = line.strip('\n').split('\t')
        if float(line[11]) < 0.05:
            if line[0] in diff:
                if diff[line[0]] in case_list and line[9] in case_list:
                    continue
                elif diff[line[0]] in hc_list and line[9] in hc_list:
                    continue
                else:
                    print(line)
                    del diff[line[0]]
            else:
                diff[line[0]] = line[9]
        else:
            continue

#print(diff)
case_tax = list()
hc_tax = list()            
    
for key in diff:
    if diff[key] in case_list:
        case_tax.append(key)
    else:
        hc_tax.append(key)

## 对患者和健康人每组的物种按照所有样本均值的大小排序，得到 R 画图的 x 轴的顺序
dt = pd.read_table('Species.rabun.xls', index_col=0)
case_order = list(dt.loc[case_tax].mean(axis=1).sort_values(ascending = False).index)
hc_order = list(dt.loc[hc_tax].mean(axis=1).sort_values(ascending = False).index)
all_order = case_order[:14] + hc_order
print(':'.join(all_order))

# 根据到的物种 ID 从丰度表里提取数据并且生成画箱线图的数据
dt = pd.read_table('Species.rabun.xls', index_col=0)
dt.loc[all_order].to_csv('diff_species_abd.txt', sep='\t')
group = pd.read_table('Mapping.txt', index_col=0)
group_dict = group.to_dict()
with open('diff_species_abd.txt', 'r') as abd, open('species_boxplot.txt', 'w') as out:
    print('ID\tAbd\tGroup', file=out)
    head = abd.readline().strip('\n').split('\t')
    for line in abd:
        line = line.strip('\n').split('\t')
        if line[0] in all_order:
            for index in range(1,len(line)):
                if float(line[index]) != 0:
                    print(line[0] + '\t'+ line[index] + '\t' + group_dict[group.columns.values[0]][head[index]], file=out)           
                else:
                    print(line[0] + '\t'+ "1e-06" + '\t' + group_dict[group.columns.values[0]][head[index]], file=out)           

### 五个物种的的处理
diff = dict()
with open('Species_MetaPhlAn2.NCA-sCAD.wilcox.test.xls') as IN:
    IN.readline()
    for line in IN:
        line = line.strip('\n').split('\t')
        if float(line[11]) < 0.05:
            diff[line[0]] = line[9]
        else:
            continue

case_list = ['sCAD', 'AMI']
hc_list = ['NCA']

with open('Species_MetaPhlAn2.NCA-AMI.wilcox.test.xls') as IN:
    IN.readline()
    for line in IN:
        line = line.strip('\n').split('\t')
        if float(line[11]) < 0.05:
            if line[0] in diff:
                if diff[line[0]] in case_list and line[9] in case_list:
                    continue
                elif diff[line[0]] in hc_list and line[9] in hc_list:
                    continue
                else:
                    print(line)
                    del diff[line[0]]
            else:
                diff[line[0]] = line[9]
        else:
            continue

#print(diff)
case_tax = list()
hc_tax = list()            

items = ["Lactobacillus_mucosae", "Lactobacillus_crispatus", "Atopobium_parvulum", "Alistipes_onderdonkii", "Pyramidobacter_piscolens"]
for key in items:
    if key in diff:
#for key in diff:
        if diff[key] in case_list:
            case_tax.append(key)
        else:
            hc_tax.append(key)

## 对患者和健康人每组的物种按照所有样本均值的大小排序，得到 R 画图的 x 轴的顺序
dt = pd.read_table('Species.rabun.xls', index_col=0)
case_order = list(dt.loc[case_tax].mean(axis=1).sort_values(ascending = False).index)
hc_order = list(dt.loc[hc_tax].mean(axis=1).sort_values(ascending = False).index)
all_order = case_order[:14] + hc_order
print(':'.join(all_order))

# 根据到的物种 ID 从丰度表里提取数据并且生成画箱线图的数据
#dt = pd.read_table('Species.rabun.xls', index_col=0)
dt.loc[all_order].to_csv('five_diff_species_abd.txt', sep='\t')
group = pd.read_table('Mapping.txt', index_col=0)
group_dict = group.to_dict()
with open('five_diff_species_abd.txt', 'r') as abd, open('five_species_boxplot.txt', 'w') as out:
    print('ID\tAbd\tGroup', file=out)
    head = abd.readline().strip('\n').split('\t')
    for line in abd:
        line = line.strip('\n').split('\t')
        if line[0] in all_order:
            for index in range(1,len(line)):
                if float(line[index]) != 0:
                    print(line[0] + '\t'+ line[index] + '\t' + group_dict[group.columns.values[0]][head[index]], file=out)           
                else:
                    print(line[0] + '\t'+ "1e-06" + '\t' + group_dict[group.columns.values[0]][head[index]], file=out)           
            

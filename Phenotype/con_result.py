# 接同时对连续型变量差异检验的文件，输出发表文章格式的表格；之所以离散型和连续型变量分开，是因为两种数据的处理方式不一样，后边再找机会看能不能合并吧；
# 输出格式为 mean(sd) ... p 值
import re
group_list = 'NS:FS:CS'.split(':')
indice = 'Age:BMI'.split(':')
out = open('Final_Result.NS-FS-CS.mixcon.xls', 'w')
dt = pd.read_table('Result.NS-FS-CS.mixcon.xls', sep = '\t', index_col = 0)
print('Characteristic\t' + '\t'.join(group_list) + '\tP value', file = out)
for x in indice:
   # print(x +',mean(sd)' + '\t'*len(group_list) + '%.2e' % dt.loc[x]['pvalue'])
    sub_dt = dt.loc[x]
    line = ''
    for group in group_list:
        Mean = 'mean('+ group + ')' 
        Sd = 'sd('+ group + ')' 
        for colname in sub_dt.index:
            if colname == Mean:
                group_mean = str(round(sub_dt[colname],2))
                line = line + '\t'+ group_mean

            if colname == Sd:
                group_sd = '('+str(round(sub_dt[colname],2))+')'
                line = line + group_sd
    print(x +',mean(sd)' + line + '\t%.2e' % dt.loc[x]['pvalue'], file = out) #科学计数法
out.close()

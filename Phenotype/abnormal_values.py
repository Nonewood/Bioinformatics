# 统计表型信息的缺失值和异常值，这里异常值的定义为 大于第三分位数 +  1.5 倍的四分位距或者小于第一分位数的 - 1.5 倍的四分位距；
#20190505 更新，阜外项目的表型信息记录
import pandas as pd 
dt = pd.read_table('phenotype.xls', index_col = 0)
# 缺失值的统计
# >10 样品以上缺失的表型信息 
nan_dt = dt.loc[:,dt.isnull().sum() > 10]
group_dt = dt['Group'].to_frame()
#type(group_dt)
group_dt
dt_merge = pd.concat([nan_dt, group_dt], axis=1)
# 统计各组的异常值数目
print('===NCA n=42 ===')
print(dt_merge.loc[dt_merge['Group'] == 'NCA'].isnull().sum())
dt_merge.loc[dt_merge['Group'] == 'NCA'].isnull().sum().to_frame(name = 'Nan Number(n = 42)').to_csv('NCA_NaN.txt', sep = "\t")
print('\n===sCAD n=54 ===')
print(dt_merge.loc[dt_merge['Group'] == 'sCAD'].isnull().sum())
dt_merge.loc[dt_merge['Group'] == 'sCAD'].isnull().sum().to_frame(name = 'Nan Number(n = 54)').to_csv('sCAD_NaN.txt', sep = "\t")
print('\n===AMI n=52 ===')
print(dt_merge.loc[dt_merge['Group'] == 'AMI'].isnull().sum())
dt_merge.loc[dt_merge['Group'] == 'AMI'].isnull().sum().to_frame(name = 'Nan Number(n = 52)').to_csv('AMI_NaN.txt', sep = "\t")
#nan_dt
#pd.concat[[dt.loc[:,'Group'],dt.loc[:,dt.isnull().sum() > 10]]]
#后边的结果需要继续优化 20190506

## 统计离群值
dt = pd.read_table('phenotype.xls', index_col = 0)
float_dt = dt.loc[:,dt.dtypes == "float64"] # 只处理浮点型变量
import numpy as np
for item in float_dt.columns: 
    Percentile = np.nanpercentile(dt[item],[0,25,50,75,100])
    IQR = Percentile[3] - Percentile[1]
    UpLimit = Percentile[3] + IQR*1.5  #最大以及最小值（下行）
    DownLimit = Percentile[1] - IQR*1.5
    abn_number = ((dt[item] > UpLimit) | (dt[item] < DownLimit)).sum()
    if abn_number  > 0:
        target_dt = dt[item].loc[(dt[item] > UpLimit) | (dt[item] < DownLimit)].to_frame(name=item)
        filename = item + '_abnormal_values.txt'
        outpath = 'Abnormal_value/' + filename
        target_dt.to_csv(outpath, sep = '\t')        

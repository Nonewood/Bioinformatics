import pandas as pd
dt = pd.read_table('braycurtis.txt', index_col=0)
expose_diversity = dt.loc[dt.index.str.contains('-a') == False, dt.columns.str.contains('-a') == False] #这个用法比较巧妙，行名不包含'-a'的行；
recovery_diversity = dt.loc[dt.index.str.contains('-a'), dt.columns.str.contains('-a')] # 行名包含 '-a' 的行；
expose_diversity.to_csv('expose_diversity', sep='\t')
recovery_diversity.to_csv('recovery_diversity', sep='\t')

#补充用法，增加单独筛选行或者列的用法，一旦不用就老是忘记....
dt = pd.read_table('genusProfileTable.xls', header = 0, index_col = 0, sep="\t")
expose_dt = dt.loc[:,dt.columns.str.contains('-a') == False]
recovery_dt = dt.loc[:,dt.columns.str.contains('-a')]   #注意冒号的使用，代表全部！
expose_dt.to_csv('expose_genusProfileTable.xls', sep='\t')
recovery_dt.to_csv('recovery_genusProfileTable.xls', sep='\t')

#增加通过正则表达式的筛选
import pandas as pd
dt = pd.read_table('expose_genusProfileTable.xls', header=0, index_col=0)
dt_F = dt.loc[:, dt.columns.str.contains('M\d',regex=True) == False]
dt_F.to_csv('expose_F_genusProfileTable.xls', sep="\t")
dt_M = dt.loc[:, dt.columns.str.contains('M\d',regex=True)]
dt_M.to_csv('expose_M_genusProfileTable.xls', sep="\t")

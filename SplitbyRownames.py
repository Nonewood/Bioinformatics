import pandas as pd
dt = pd.read_table('braycurtis.txt', index_col=0)
expose_diversity = dt.loc[dt.index.str.contains('-a') == False, dt.columns.str.contains('-a') == False] #这个用法比较巧妙，行名不包含'-a'的行；
recovery_diversity = dt.loc[dt.index.str.contains('-a'), dt.columns.str.contains('-a')] # 行名包含 '-a' 的行；
expose_diversity.to_csv('expose_diversity', sep='\t')
recovery_diversity.to_csv('recovery_diversity', sep='\t')

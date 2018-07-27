from scipy.spatial import distance
import pandas as pd
dt = pd.read_table('GeneCatalog_profile.xls')
dt.index = dt['geneID']
dt.drop(['geneID'], axis=1, inplace=True)
with open('braycurtis.txt', 'w') as bray:
    print('\t' + '\t'.join(dt.columns.values), file = bray)
    for first in dt.columns.values:
        lst = list()
        lst.append(first)
        for second in dt.columns.values:
            dis = distance.braycurtis(dt[first], dt[second])
            lst.append(str(dis))
        print('\t'.join(lst), file=bray)

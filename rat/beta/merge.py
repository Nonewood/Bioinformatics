import pandas as pd
#合并组间或组内的距离文件
ACK = pd.read_table('ACK-ACK.distance.txt', header=0, index_col=0)
EL = pd.read_table('EL-EL.distance.txt', header=0, index_col=0)
Cig = pd.read_table('Cig-Cig.distance.txt', header=0, index_col=0)
merge = pd.concat([ACK,EL,Cig])
merge.to_csv('intra_group.txt', sep='\t')

ACK_Cig = pd.read_table('ACK-Cig.distance.txt', header=0, index_col=0)
ACK_EL = pd.read_table('ACK-EL.distance.txt', header=0, index_col=0)
EL_Cig = pd.read_table('EL-Cig.distance.txt', header=0, index_col=0)
two_merge = pd.concat([ACK_Cig,ACK_EL,EL_Cig])
two_merge.to_csv('inter_group.txt', sep='\t')

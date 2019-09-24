## beta 多样性矩阵文件处理, 输出用于画箱线图的组内和组间的距离文件
import pandas as pd
dt = pd.read_table('braycurtis.txt', index_col = 0)  #距离矩阵文件
group = pd.read_table('info.xls', index_col=0) #表型文件
group_dict = group['Group'].to_dict() #生成样品-组名的字典

##两两样品名作为键，距离值作为值，生成字典..
distance = dict()
for Id1 in dt.columns:
    for Id2 in dt.columns:
        key = Id1 + ':' + Id2
        key_temp = Id2 + ':' + Id1
        value = dt.loc[Id1,Id2]
        if (key in distance) or (key_temp in distance): # 判断是否有重复的
            continue
        else:
            distance[key] = value
            
out = open('intra_distance.txt','w')  # 生成画 boxplot 的文件
print('individuals\tdistance\tgroup', file=out)
n = 0
for key in distance:
    key_split = key.split(':')
    if key_split[0] == key_split[1]: #如果是同一个体, 则跳过；
        n = n +1
        continue
    if group_dict[key_split[0]] ==  group_dict[key_split[1]]:  #判断是否同组,
        print('\t'.join([key, str(distance[key]), group_dict[key_split[0]]]), file=out)
    else:
        print('\t'.join([key, str(distance[key]), 'sCAD-AMI']), file=out)  #否的话，输出组间样品距离的值
#print(n) #测试用
out.close()

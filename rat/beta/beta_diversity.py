#! /usr/bin/python3
#将总的距离文件按照组别分组并且生成用于画图的组间和组内的表格
import pandas as pd
import sys
beta_diversityfile = sys.argv[1]
outdir = sys.argv[2]
par = [beta_diversityfile,outdir]
if not all (par):
	print('you silly fool!')
	exit()

dt = pd.read_table(beta_diversityfile, header=0, index_col=0)
expose_diversity = dt.loc[dt.index.str.contains('-a') == False, dt.columns.str.contains('-a') == False] #这个用法比较巧妙，行名不包含'-a'的行；
recovery_diversity = dt.loc[dt.index.str.contains('-a'), dt.columns.str.contains('-a')] # 行名包含 '-a' 的行；
Fexpose_diversity = expose_diversity.loc[expose_diversity.index.str.contains('F\d'),expose_diversity.columns.str.contains('F\d')]
Mexpose_diversity = expose_diversity.loc[expose_diversity.index.str.contains('M\d'),expose_diversity.columns.str.contains('M\d')]
Frecovery_diversity = recovery_diversity.loc[recovery_diversity.index.str.contains('F\d'),recovery_diversity.columns.str.contains('F\d')]
Mrecovery_diversity = recovery_diversity.loc[recovery_diversity.index.str.contains('M\d'),recovery_diversity.columns.str.contains('M\d')]

def distance_cal(dt,temp):
	distance = dict()
	for Id1 in dt.columns:
		for Id2 in dt.columns:
			key = Id1 + ':' + Id2
			key_temp = Id2 + ':' + Id1
			value = dt.loc[Id1,Id2]
			if (key in distance) or (key_temp in distance):
				continue
			else:
				distance[key] = value
	ACK_ACK = open(temp + '/ACK-ACK.distance.txt','w')
	print('individuals\tdistance\tgroup', file=ACK_ACK)
	EL_EL = open(temp +'/EL-EL.distance.txt','w')
	print('individuals\tdistance\tgroup', file=EL_EL)
	Cig_Cig = open(temp + '/Cig-Cig.distance.txt','w')
	print('individuals\tdistance\tgroup', file=Cig_Cig)
	ACK_EL = open(temp + '/ACK-EL.distance.txt','w')
	print('individuals\tdistance\tgroup', file=ACK_EL)
	ACK_Cig = open(temp + '/ACK-Cig.distance.txt','w')
	print('individuals\tdistance\tgroup', file=ACK_Cig)
	EL_Cig = open(temp + '/EL-Cig.distance.txt','w')
	print('individuals\tdistance\tgroup', file=EL_Cig)

	for key in distance:
		key_split = key.split(':')
		if key_split[0] == key_split[1]:
			continue
		if key_split[0].startswith('ACK') and key_split[1].startswith('ACK'):
			print(key + '\t' + str(distance[key]) + '\t' + 'ACK', file=ACK_ACK)
		elif key_split[0].startswith('EL') and key_split[1].startswith('EL'):
			print(key + '\t' + str(distance[key]) + '\t' + 'EL', file=EL_EL)
		elif key_split[0].startswith('Cig') and key_split[1].startswith('Cig'):
			print(key + '\t' + str(distance[key]) + '\t' + 'Cig', file=Cig_Cig)
		elif (key_split[0].startswith('ACK') and key_split[1].startswith('EL')) or (key_split[0].startswith('EL') and key_split[1].startswith('ACK')):
			print(key + '\t' + str(distance[key]) + '\t' + 'ACK-EL', file=ACK_EL)
		elif (key_split[0].startswith('ACK') and key_split[1].startswith('Cig')) or (key_split[0].startswith('Cig') and key_split[1].startswith('ACK')):
			print(key + '\t' + str(distance[key]) + '\t' + 'ACK-Cig', file=ACK_Cig)
		elif (key_split[0].startswith('EL') and key_split[1].startswith('Cig')) or (key_split[0].startswith('Cig') and key_split[1].startswith('EL')):
			print(key + '\t' + str(distance[key]) + '\t' + 'El-Cig', file=EL_Cig)
	ACK_ACK.close()
	EL_EL.close()
	Cig_Cig.close()
	ACK_EL.close()
	ACK_Cig.close()
	EL_Cig.close()

import re
lst = ['Fexpose_diversity','Mexpose_diversity','Frecovery_diversity','Mrecovery_diversity']
dts = [Fexpose_diversity,Mexpose_diversity,Frecovery_diversity,Mrecovery_diversity]
for index in range(len(lst)):
	if re.search('(.*)_diversity',lst[index]):
		match = re.search('(.*)_diversity',lst[index])
		temp = outdir + '/' +  match.group(1)
		distance_cal(dts[index],temp)

import pandas as pd

#F_expose
F_expose = pd.read_table('F_expose_phylumProfileTable.xls', header=0, sep="\t", index_col = 0)
F_expose_FB = F_expose.loc[['Firmicutes']]/F_expose.loc[['Bacteroidetes']].values # 两行相除，这个用法需要记住
F_expose_FB.index = ['FB']
F_expose_FB_T = F_expose_FB.T

#M_expose
M_expose = pd.read_table('M_expose_phylumProfileTable.xls', header=0, sep="\t", index_col = 0)
M_expose_FB = M_expose.loc[['Firmicutes']]/M_expose.loc[['Bacteroidetes']].values
M_expose_FB.index = ['FB']
M_expose_FB_T = M_expose_FB.T

#F_recovery
F_recovery = pd.read_table('F_recovery_phylumProfileTable.xls', header=0, sep="\t", index_col = 0)
F_recovery_FB = F_recovery.loc[['Firmicutes']]/F_recovery.loc[['Bacteroidetes']].values
F_recovery_FB.index = ['FB']
F_recovery_FB_T = F_recovery_FB.T

M_recovery = pd.read_table('M_recovery_phylumProfileTable.xls', header=0, sep="\t", index_col = 0)
M_recovery_FB = M_recovery.loc[['Firmicutes']]/M_recovery.loc[['Bacteroidetes']].values
M_recovery_FB.index = ['FB']
M_recovery_FB_T = M_recovery_FB.T

merge = pd.concat([F_expose_FB_T,M_expose_FB_T,F_recovery_FB_T,M_recovery_FB_T])
merge.to_csv('F_B_ratio.txt', sep="\t")

import re
with open('F_B_ratio.txt','r') as IN, open('F_B_ratio_boxplot.txt','w') as out:
	head = IN.readline().strip('\n').split('\t')[1]
	print('SampleID\t' + head + '\tsubgroup\tgroup', file=out)
	for line in IN:
		lst = line.strip('\n').split('\t')
		if not lst[0].endswith('-a'):
			if re.match('Cig\-F', lst[0]):
				subgroup = 'Cigarette'
				group = 'F_expose'  # 根据命名分组，不具有普适性... 
			elif re.match('Cig\-M', lst[0]):
				subgroup = 'Cigarette'
				group = 'M_expose'
			elif re.match('EL\-F', lst[0]):
				subgroup = 'E-liquid'
				group = 'F_expose'
			else:
				subgroup = 'E-liquid'
				group = 'M_expose'
		else:
			if re.match('Cig\-F', lst[0]):
				subgroup = 'Cigarette'
				group = 'F_recovery'
			elif re.match('Cig\-M', lst[0]):
				subgroup = 'Cigarette'
				group = 'M_recovery'
			elif re.match('EL\-F', lst[0]):
				subgroup = 'E-liquid'
				group = 'F_recovery'
			else:
				subgroup = 'E-liquid'
				group = 'M_recovery'
		outline = '\t'.join([lst[0],lst[1],subgroup,group])
		print(outline, file=out)

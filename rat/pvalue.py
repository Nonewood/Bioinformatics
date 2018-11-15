#! /usr/bin/python3
import pandas as pd
import glob,re
lst = ['F_shannon','M_shannon','F_number','M_number']
for item in lst:
	sex = item.split('_')[0]
	arf = item.split('_')[1]

# homogeneity p value
	for time in ['expose','recovery']:
		prefix = sex + time +'_homogeneity_' + arf
		filename = prefix + '.txt'
		with open(filename, 'r') as homogeneity:
			dt = pd.read_table(homogeneity, header=0, index_col=0)
			homogeneity_p = dt['Pr(>F)'][1]
			print(prefix + ':')
			print(homogeneity_p)
#normality
	for time in ['expose','recovery']:
		prefix = sex + time + '_normality_' + arf
		filename = prefix + '.txt'
		with open(filename, 'r') as normality:
			dt = pd.read_table(normality, header=0, index_col=0)
			normality_p = dt['p.value'][0]
			print(prefix + ':')
			print(normality_p)
	
# annova
	for time in ['expose','recovery']:
		prefix = sex + time + '_anova_' + arf
		filename = prefix + '.txt'
		with open(filename, 'r') as anova:
			dt = pd.read_table(anova, header=0, index_col=0)
			anova_p = dt['Pr(>F)'][0]
			print(prefix + ':')
			print(anova_p)

# Tukey
	for time in ['expose','recovery']:
		prefix = sex + time +'_Tukey_' + arf
		filename = prefix + '.txt'
		with open(filename, 'r') as Tukey:
			dt = pd.read_table(Tukey, header=0, index_col=0)
			Tukey_p = dt['Group.p adj']
			print(prefix + ':')
			print(Tukey_p)

	print('========')

#! /usr/bin/python3
#根据分组名字，合并组间组内的距离文件，并且运行 anova.R
import os,sys
parent_dierctory = sys.argv[1]
title = sys.argv[2] #
items = ['Fexpose','Frecovery','Mexpose','Mrecovery']
for directory in items:
	os.chdir(parent_dierctory + '/' + directory)
	os.system('python3 merge.py')
	os.system('Rscript anova.R intra_group.txt ' + directory +'_intra ' + title + ' ACK:EL:Cig distance group')
	os.system('Rscript anova.R inter_group.txt ' + directory +'_inter ' + title + ' ACK-Cig:ACK-EL:El-Cig distance group')

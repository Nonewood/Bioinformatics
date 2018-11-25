#! /usr/bin/python3
import sys,os,shutil
if len(sys.argv) != 3:
    print('you silly fool~~ (hahaha kidding,please check your parameters)')
    exit()
betadir = sys.argv[1]
abdfile = sys.argv[2]
title = sys.argv[3]
os.chdir(betadir)
if not os.path.exists('Outdir'):
	os.makedirs('Outdir')
else:
	shutil.rmtree('Outdir')
	os.makedirs('Outdir')
#generate the distance file
os.system('python3 braycurtis.py -i ' + abdfile)

os.chdir('Outdir')
os.system('mkdir Fexpose Mexpose Frecovery Mrecovery')

#split the distance file
os.system('python3 beta_diversity.py ../braycurtis.txt ./')

#merge the distance file and run anova
parent_dir = betadir + '/Outdir'
os.system('python3 process.py ' + parent_dir + ' ' + title)

#scp the pdf files to Mac
os.system('sh scp.sh')

# print p values
os.system('python3 pvalue.py ' + parent_dir + '>' + parent_dir + '/pvalue.txt')

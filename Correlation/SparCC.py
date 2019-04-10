#使用 SparCC 计算相关性，https://bitbucket.org/yonatanf/sparcc/overview
##usage: python /Users/tongxueer/Documents/R/run_sparcc.py example/fake_data.txt fake outdir
### 运行该脚本比较麻烦...需要特定的 Python 版本以及相应的库版本，查到了使用 conda 进入虚拟环境的解决办法（还是挺方便的，除了每次都得进入比较麻烦）
### 
$ conda create --name SparCC python=2.6.9
$ source activate SparCC
$ conda install python-dateutil=2.4.2
$ conda install numpy=1.9.2 pandas=0.16.2
$ conda install libcxx
####

import sys,os
abdfile = sys.argv[1] #/Users/tongxueer/Documents/R/p_0.05.new.name.profile.xls
prefix = sys.argv[2] # mgs
outdir = sys.argv[3] # ./
if not os.path.exists(outdir):
	os.makedirs(outdir)

sparcc = outdir + '/' + prefix + '_sparcc.txt'
cov_sparcc = outdir + '/' +prefix + '_cov_sparcc.txt'
os.system('python /Users/tongxueer/Documents/R/yonatanf-sparcc-3aff6141c3f1/SparCC.py ' + abdfile + ' -c ' + sparcc + ' -v ' + cov_sparcc)

#repeat 100
output = outdir + '/pseudo'
if not os.path.exists(output):
	os.makedirs(output)
os.system('python /Users/tongxueer/Documents/R/yonatanf-sparcc-3aff6141c3f1/MakeBootstraps.py ' +  abdfile + ' -p ' + output  + '/ -t permuted_#')

corr_dir = outdir + '/boot_' + prefix + '_corr'
if not os.path.exists(corr_dir):
	os.makedirs(corr_dir)
cov_dir =  outdir + '/boot_' + prefix + '_cov'
if not os.path.exists(cov_dir):
	os.makedirs(cov_dir)
os.system('for i in `seq 0 99`; do python /Users/tongxueer/Documents/R/yonatanf-sparcc-3aff6141c3f1/SparCC.py ' + output + '/permuted_$i -c ' + corr_dir + '/simulated_sparcc_$i.txt -v ' + cov_dir + '/simulated_sparcc_$i.txt >> ' + outdir + '/' + prefix + '_boot_sparcc.log; done')

pvals_dir = outdir + '/' + prefix + '_pvals'
if not os.path.exists(pvals_dir):
	os.makedirs(pvals_dir)
os.system('python /Users/tongxueer/Documents/R/yonatanf-sparcc-3aff6141c3f1/PseudoPvals.py ' + sparcc+ ' ' + corr_dir + '/simulated_sparcc_#.txt 100 -o ' + pvals_dir + '/one_sided.txt -t one_sided')

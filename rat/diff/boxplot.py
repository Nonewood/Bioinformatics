#! /usr/bin/python3 
import argparse,re,numpy,os
import pandas as pd
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
generate the boxplot based on different test.
Example: python3 barplot.py -i phylumProfileTable.xls -o Process -r 0.01
To be continued.
------------------'''
)
parser.add_argument('-a','--abd', help = "the abundance file, eg M_expose_genusProfileTable.xls.")
parser.add_argument('-g','--group', help = "the group name,eg EL:Cig.")
parser.add_argument('-c','--color', help = "the color scheme,eg 487eb3:d2382c.")
parser.add_argument('-d','--diff', help = "the filtered different test result file, eg filter_EL_Cig.E-liquid-Cigarette.wilcox.test.xls.")
parser.add_argument('-n','--number', help = "the number of tax for boxplot,eg 20. default is 20.", nargs='?')
parser.add_argument('-f','--filter_type', help = "the filter type of different result,eg pvalue. default is qavlue", nargs='?')
parser.add_argument('-o','--outdir', help = "the output directory")
args=parser.parse_args()
(abd_file,group,color,diff_result,outdir) = (args.abd,args.group,args.color,args.diff,args.outdir)
par = [abd_file,group,color,diff_result,outdir]
if not all(par):
	parser.print_help()
	exit()

tax_number = args.number if args.number else 20
filter_type = args.filter_type if args.filter_type else 'qvalue'

os.chdir(outdir)
group_list = group.split(':')
with open(abd_file, 'r') as abd, open('tax_mean_order.txt','w') as out:
    out.write('Tax\tMean\n')
    head = abd.readline().strip('\n').split('\t')
    for line in abd:
        line = line.strip('\n').split('\t')
        control_list = list()
        case_list = list()
        for index in range(1,len(line)):
            if re.match('EL',head[index]):
                control_list.append(float(line[index]))
            else:
                case_list.append(float(line[index]))
        out.write(line[0] + '\t' + str(numpy.mean(control_list)) + '\n')
        out.write(line[0] + '\t' + str(numpy.mean(case_list)) + '\n')
        
mean_order = pd.read_table('tax_mean_order.txt', header=0, index_col=0)
plot_tax = numpy.unique(mean_order.sort_values(by = 'Mean', ascending=False)[:tax_number*2].index)[:tax_number]

with open(abd_file, 'r') as abd, open('boxplot.txt', 'w') as out:
    print('ID\tAbd\tGroup\n', file=out)
    head = abd.readline().strip('\n').split('\t')
    for line in abd:
        line = line.strip('\n').split('\t')
        if line[0] in plot_tax:
            for index in range(1,len(line)):
                if re.match(group_list[0],head[index]):
                    print(line[0] + '\t'+ line[index] + '\t' + group_list[0], file=out)
                else:
                    print(line[0] + '\t'+ line[index] + '\t' + group_list[1], file=out)

rscript = 'Rscript boxplot.R boxplot.txt ' + group + ' ' + color + ' ' + diff_result + ' ' + filter_type
print(rscript)
os.system(rscript)
# 删除过程文件
os.remove('boxplot.txt')
os.remove('tax_mean_order.txt')

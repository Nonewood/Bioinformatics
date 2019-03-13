#! /usr/bin/python3 
import argparse,re
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
generate the barplot based on abundance file.
Example: python3 barplot.py -i phylumProfileTable.xls -o Process -r 0.01
To be continued.
------------------'''
)
#parser = argparse.ArgumentParser(description = "based on the abundance file,get the tax ID for with relative abundance bigger than some value(eg: 0.01)  at least in one sample, tax with relative abundance less than this values will be merged as others in next step.")
#parser = argparse.ArgumentParser(description = "based on the abundance file,get the tax ID for with abundance bigger than some value(eg: 0.01)  at least in one sample, for the x axis text of barplot of  before and after two groups...not very clear.") +_+|| 确实没看懂..
parser.add_argument('-i','--Input', help = "the input file")
parser.add_argument('-r','--rate', help = "the value for selecting tax ID, default in 0.", nargs='?')
parser.add_argument('-o','--Output', help = "the output directory")
args=parser.parse_args()
(Input,Output) = (args.Input,args.Output)

rate = args.rate if args.rate else 0

if not Input or not Output:
	parser.print_help() 
	exit()

'''
import os,shutil
if os.path.exists(Output):
	shutil.rmtree(Output)
os.makedirs(Output)
'''

# get the tax ID needed!
match = re.match('(.*)ProfileTable',Input.split("/")[-1])
level = match.group(1)
IDlist = list()
with open(Input,'r') as IN:
	IN.readline()
	for line in IN:
		lst = line.strip('\n').split('\t')
		for index in range(1,len(lst)):
			if float(lst[index]) > float(rate) :
				IDlist.append(lst[0])
				break
			else:
				continue

# output the barplot.txt file
outfile = Output +'/' + level + "Barplot.txt"
with open(Input, "r") as IN, open(outfile, "w") as out:
	out.write('individual\tlevel\tabundance\n')
	head = IN.readline().strip('\n').split('\t')
	Dict = dict()
	for element in head[1:]:
		Dict[element] = 0
	for line in IN:
		lst = line.strip('\n').split('\t')
		taxonomy = lst[0]
		for index in range(1,len(lst)):
			if taxonomy not in IDlist:
				Dict[head[index]] = Dict[head[index]] + float(lst[index])
			else:
				key = head[index] + "\t" + taxonomy + "\t" + lst[index]
				Dict[key] = head[index]
	for key in Dict:
		if key in head and Dict[key] == 0:
			continue
		elif key in head:
			out.write(key + '\tOthers\t' + str(Dict[key]) + '\n')
		else:
			keys = key.split('\t')
			indiv = keys[0]
			taxonomy = keys[1]
			abund = keys[2]
			out.write(indiv + '\t' + taxonomy + '\t' + abund + '\n')

# get the taxID order and sampleID order for drawing barplot
import pandas as pd
dt = pd.read_table(outfile)
tax_order = list(dt.groupby('level').abundance.mean().sort_values(ascending=False).index)
if 'Others' in tax_order:
	tax_order.remove('Others')
	tax_order.append('Others')
sample_order = list(dt.loc[dt['level'] == tax_order[0]].groupby('individual').abundance.mean().sort_values().index)

#generate barplot Rscript
color_list = list()
with open('color.txt', 'r') as color:
	color_list = color.read().split('\n')  # 一次性读取文件

color_list.pop(-1)
color_list = color_list[:len(tax_order)]
plot_tax_order = ','.join(['"' + x + '"' for x in tax_order])
plot_sample_order = ','.join(['"' + x + '"' for x in sample_order])
plot_color = ','.join(['"' + x + '"' for x in color_list])
outplot = Output +'/' + level + 'Barplot.pdf'
plot_script = Output +'/' + level + 'ProfileBarplot.R'
with open(plot_script, 'w') as rscript:
	print('#! /usr/bin/Rscript', file=rscript)
	print('dt = read.table("' + outfile + '",header = T, sep = "\\t")', file=rscript)
	print('library(ggplot2)', file=rscript)
	print('sampleID = c(' + plot_sample_order + ')', file=rscript)
	print('legendID = c(' + plot_tax_order + ')', file=rscript)
	print('color = c(' + plot_color + ')', file=rscript)
	print('dt$individual_order = factor(dt$individual, level=sampleID)', file=rscript)
	print('ggplot(dt,aes(x=dt$individual_order,y=dt$abundance,fill=factor(dt$level,levels=rev(legendID)))) + geom_bar(stat = "identity", color = "#56666B", size = 0.1)  + labs(x = "Inidividuals", y = "Relative Abundance") + theme_bw() + theme(axis.title = element_text(size = 12), axis.text = element_text(colour = "black", size = 10), axis.text.x = element_text(hjust = 1,angle=65,color="black"),legend.title = element_blank(),legend.key.size=unit(3,"mm"), legend.text=element_text(size=10)) + scale_fill_manual(values = rev(color))', file=rscript)
	print('ggsave("' + outplot + '", width=6, height=4)', file=rscript)
	print('unlink("Rplots.pdf")', file=rscript)

# plot 
import os
os.system('Rscript ' + plot_script)

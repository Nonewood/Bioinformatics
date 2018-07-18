# 统计丰度表中，所有大于 1（1%）的物种的 ID, 画柱状图时, 需要把在所有样品中小于 1% 的物种合并为 others, 想了半天才想起来这个脚本的功能，必须得做好日志文件呀.
# 通用性不高，记在此处只是当做记录脚本.
#! /usr/bin/python3
import argparse,re
parser = argparse.ArgumentParser(description = "based on the abundance file,get the species ID for with abundance > 1% in any of sample, for the x axis text of barplot of  before and after two groups...not very clear.")
parser.add_argument('-i','--Input', help = "the input file")
parser.add_argument('-o','--Output', help = "the output directory")
args=parser.parse_args()
(Input,Output) = (args.Input,args.Output)
if not Input or not Output:
    print("Plase add the parameters,thank you :)\n\nExample: python3 plotIdGenerate.py -i /ifshk5/BC_COM_P11/F17HTSCCWLJ1810/RATdkdM/MetaPhlAn2/process/Taxonomy_MetaPhlAn2/MetaPhlAn2_Analysis/All/GoALL/phylumProfileTable.xls  -o /ifshk5/BC_COM_P11/F17HTSCCWLJ1810/RATdkdM/MetaPhlAn2/process/Taxonomy_MetaPhlAn2/MetaPhlAn2_Analysis\n")
    exit()
match = re.match('(.*)ProfileTable',Input.split("/")[-1])
outfile = Output + '/' + match.group(1) + 'ID'
with open(Input,'r') as IN,open(outfile,'w') as out:
    IN.readline()
    for line in IN:
        lst = line.strip('\n').split('\t')
        for index in range(1,len(lst)):
            if float(lst[index]) > 1:
                out.write(lst[0]+"\n")
                break
            else:
                next

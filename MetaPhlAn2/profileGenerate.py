#基于 MetaPhlan2 合并后的文件输出不同水平的丰度表, 目前只有三个水平，门，属，种
#! /usr/bin/env python3
import argparse,re
parser = argparse.ArgumentParser(description = "get the abundance file of some level of microbes from MetaPhlAn2_Merge_abundance_table  ... To be continued!")
parser.add_argument('-i','--Input', help = "the input file")
parser.add_argument('-o','--Output', help = "the output directory")
parser.add_argument('-l','--level', help = "the level of species,separated by a comma,like: phylum,genus,species")
args=parser.parse_args()
(Input,Output,level) = (args.Input,args.Output,args.level)
if not Input or not Output or not level:
    print("Plase add the parameters,thank you :)\n\nExample: python3 genus_abundance.py -i MetaPhlAn2_Analysis/MetaPhlAn2_Merge_abundance_table.xls -l phylum,genus,species -o Taxonomy_MetaPhlAn2/MetaPhlAn2_Analysis\n")
    exit()

level_list = list()
if re.search(",",level):
	level_list = level.split(",")
else:
	level_list = level

#=======genus=====
if "genus" in level_list:
	print("producing the genus abundance file")
	with open(Input,'r') as IN, open (Output + "genusProfileTable.xls",'w') as out:
		IN.readline()
		head = IN.readline()
		out.write(head)
		for line in IN:
				if len(line.strip('\n').split('\t')[0].split('|')) == 6:
					genus = line.strip('\n').split('\t')[0].split('|')[-1]
					lst = line.strip('\n').split('\t')
					out.write(genus)
					for index in range(1,len(lst)):
						out.write('\t' + lst[index])
					out.write('\n')
				else:
					continue;
	print("producing the genus abundance file is done!")
else:
	print("not genus here!")
#=======phylum=====
if "phylum" in level_list:
    print("producing the phylum abundance file")
    with open(Input,'r') as IN,open (Output + "phylumProfileTable.xls",'w') as out:
        IN.readline()
        head = IN.readline()
        out.write(head)
        for line in IN:
                if len(line.strip('\n').split('\t')[0].split('|')) == 2:
                    phylum = line.strip('\n').split('\t')[0].split('|')[-1]
                    lst = line.strip('\n').split('\t')
                    out.write(phylum)
                    for index in range(1,len(lst)):
                        out.write('\t' + lst[index])
                    out.write('\n')
                else:
                    continue;
    print("producing the phylum abundance file is done!")
else:
	print("not phylum here!")
#=======species=====
if "species" in level_list:
    print("producing the species abundance file")
    with open(Input,'r') as IN,open (Output + "speciesProfileTable.xls",'w') as out:
        IN.readline()
        head = IN.readline()
        out.write(head)
        for line in IN:
                if len(line.strip('\n').split('\t')[0].split('|')) == 7:
                    species = line.strip('\n').split('\t')[0].split('|')[-1]
                    lst = line.strip('\n').split('\t')
                    out.write(species)
                    for index in range(1,len(lst)):
                        out.write('\t' + lst[index])
                    out.write('\n')
                else:
                    continue;
    print("producing the species abundance file is done!")
else:
	print("not species here!")

#! /usr/bin/python3

import pandas as pd
import rpy2.robjects as robjects
import numpy as np
from itertools import combinations
from collections import defaultdict
import argparse,os,math

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description='''
-------------------
Simple Introduction:
Generate the core OTU results.
Example: python3 core_OTU.py -i filter_OTU_shared_final.xls -g plant.bms.txt.all.new.name -s SubGroup3 -p SubGroup1 -o outdir
To be continued.
------------------'''
)

parser.add_argument('-i','--Input', help = "the OTU abundance file, eg filter_OTU_shared_final.xls.")
parser.add_argument('-g','--group', help = "the group file,eg plant.bms.txt.all.new.name.")
parser.add_argument('-s','--sample', help = "the column name of  sample ID line,eg SubGroup3.")
parser.add_argument('-p','--groupname', help = "the column name of group name for analysis,eg SubGroup1.")
parser.add_argument('-t','--threshold', help = "threshold for core OTU, default is 0.8.", type = float, nargs = "?")
parser.add_argument('-o','--outdir', help = "the output directory", nargs = "?")
args=parser.parse_args()

(otu_file, group_file, sample_ID, group_par) = (args.Input, args.group, args.sample ,args.groupname)

par = [otu_file, group_file, sample_ID, group_par]
if not all(par):
		parser.print_help()
		exit()

threshold  = args.threshold if args.threshold else 0.8
outdir = args.outdir if args.outdir else './'
if not os.path.exists(outdir):
	os.mkdir(outdir)

# merge OTU table for samples with repeat
def merge_otu(group_file, otu_file, sample_ID, outdir):
	sample = dict()
	with open(group_file, 'r') as IN:
		group_header = IN.readline().strip('\n').split('\t')
		sampleID_index =  group_header.index(sample_ID)
		for line in IN:
			lst = line.strip('\n').split('\t')
			sample[lst[0]] = lst[sampleID_index]
	with open(otu_file, 'r') as IN, open(outdir + '/merge_OTU_profile.txt', 'w') as out:
		otu_header = IN.readline().strip('\n').split('\t')
		sample[otu_header[0]] = otu_header[0]
		new_header = [sample[x] for x in otu_header if x in sample]
		Remove_duplicates = list(set(new_header))
		Remove_duplicates.remove(new_header[0])
		out_header = otu_header[0] + '\t' + '\t'.join([str(x) for x in sorted(Remove_duplicates)])  ##import of sort
		print(out_header, file=out)
		for line in IN:
			lst = line.strip('\n').split('\t')
			outID = lst[0]
			zeroINsample = list()
			counts = defaultdict(float) # value will initialize to 0
			sum = defaultdict(float)
			mean_OTU = dict()
			for x in range(1,len(lst)):
				if lst[x] == '0':
					zeroINsample.append(new_header[x])
				counts[new_header[x]] += 1
				sum[new_header[x]] += float(lst[x])
			equal = out_header.split('\t')
			equal.remove(new_header[0])
			if equal != sorted(counts.keys()):
				print('Something wrong! Please contact me~')
				exit()
			for key in sorted(counts.keys()): #here to be sort for consistent
				if key not in zeroINsample:
					mean = sum[key]/counts[key]
					mean_OTU[key] = mean
				else:
					mean_OTU[key] = 0
			out_list = list()
			for key in sorted(mean_OTU.keys()):
				out_list.append(mean_OTU[key])
			out_line = outID + '\t' + '\t'.join([str(x) for x in out_list])
			print(out_line, file=out)
	print("Generate merged OTU table: " + "merge_OTU_profile.txt")

# common otu table
def common_OTU(group_par, sample_ID, threshold, outdir):
	common_OTU_list = list()
	all_groups = group[group_par].unique()
	for item in all_groups:
		lst = group.loc[group[group_par] == item,:][sample_ID].unique()
		sub_dt = dt[lst]
		sample_num = sub_dt.shape[1]
		threshold = sample_num*threshold
		temp_OTU = sub_dt[(sub_dt != 0).sum(axis = 1) > threshold]
		common_OTU_list = list(temp_OTU.index) + common_OTU_list
	final_OTU = list(set(common_OTU_list))
	common_OTU_dt = dt.loc[final_OTU,:]
	outfile = '_'.join(all_groups) + '_commonOTU.xls'
	common_OTU_dt.to_csv(outdir + '/' + outfile, sep ='\t')
	print("Generating the common OTU file: " + outfile)

# stat the each two group core OTU
def core_otu(compare_group, group_par, sample_ID, common_OTU, outdir):
	common_OTU_dt = pd.read_table(common_OTU, index_col=0, sep = '\t')
	#(compare_group, group_par, sample_ID) = (group_info, group_par, sample_ID)
	former_group = compare_group[0]
	latter_group = compare_group[1]
	head = ['otuID', 'mean(' + former_group + ')', 'sd(' + former_group + ')', 'mean-rank(' + former_group + ')', 'occ-rate(' + former_group + ')','mean(' + latter_group + ')', 'sd(' + latter_group + ')', 'mean-rank(' + latter_group + ')', 'occ-rate(' + latter_group + ')', 'enrcihed', 'pvalue']
	out_header = '\t'.join(head)
	out = open('_'.join(compare_group) + '_temp_diff.xls', 'w')
	print(out_header, file = out)
	for otu in common_OTU_dt.index:
		former_lst = group.loc[group[group_par] == former_group,:][sample_ID].unique()
		latter_lst = group.loc[group[group_par] == latter_group,:][sample_ID].unique()
		former_abd = common_OTU_dt.loc[otu][former_lst]
		latter_abd = common_OTU_dt.loc[otu][latter_lst]

	#calcultate mean
		former_mean = former_abd.mean()
		latter_mean = latter_abd.mean()

	#calculate sd
		former_sd = former_abd.std()
		latter_sd = latter_abd.std()

	# calculate occurrence
		former_occ = (former_abd != 0).sum()/len(former_abd)
		latter_occ = (latter_abd != 0).sum()/len(latter_abd)

	# calculate rank for enrich
		rank = robjects.r['rank']
		two_lst = list(common_OTU_dt.loc[otu][list(former_lst) + list(latter_lst)])
		Rank = list(np.array(rank(robjects.FloatVector(two_lst))))
		former_rank = Rank[:len(list(former_lst))]
		latter_rank = Rank[len(list(former_lst)):]
		former_rank_mean = np.mean(former_rank)
		latter_rank_mean = np.mean(latter_rank)
		if former_rank_mean  > latter_rank_mean:
			enrich = former_group
		elif former_rank_mean  < latter_rank_mean:
			enrich = latter_group
		else:
			enrich = 'None'

	# calculate the pvalue
		former_vector = robjects.FloatVector(list(former_abd))
		latter_vector = robjects.FloatVector(list(latter_abd))
		wilcox = robjects.r['wilcox.test']
		pvalue = np.array(wilcox(former_vector,latter_vector)[2])[0]
		if not math.isnan(pvalue):
			line = [otu,former_mean, former_sd, former_rank_mean, former_occ, latter_mean, latter_sd, latter_rank_mean, latter_occ, enrich, pvalue]
			line = [str(x) for x in line]
			out_line = '\t'.join(line)
			print(out_line, file = out)
	out.close()

	# calculate the q value
	dt_pvalue = pd.read_table('_'.join(compare_group) + '_temp_diff.xls', sep='\t', index_col=0)
	p_adjuste = robjects.r('p.adjust')
	qvalue = p_adjuste(robjects.FloatVector(list(dt_pvalue['pvalue'])))
	dt_pvalue['qvalue'] = qvalue
	outfile = '_'.join(compare_group) + '_diff.xls'
	dt_pvalue.to_csv(outdir + '/' + outfile, sep='\t')
	os.remove('_'.join(compare_group) + '_temp_diff.xls')
	print("Generate the final results: " + outfile)

# process the otu table
merge_otu(group_file, otu_file, sample_ID, outdir)

# common OTU
dt = pd.read_table(outdir + '/merge_OTU_profile.txt', header = 0, index_col = 0, sep = '\t')
group = pd.read_table(group_file, header = 0, index_col = 0, sep = '\t')
group_par = group_par
sample_ID = sample_ID
threshold = float(threshold)

all_groups = group[group_par].unique()
common_OTU(group_par, sample_ID, threshold, outdir)
common_OTU_file = outdir + '/' + '_'.join(all_groups) + '_commonOTU.xls'

# core OTU
for compare_group in combinations(all_groups, 2):
	core_otu(compare_group,group_par, sample_ID, common_OTU_file, outdir)

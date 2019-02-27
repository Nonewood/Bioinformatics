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
Example: python3 core_OTU.py -i phylumProfileTable.xls -o Process -r 0.01
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

(abd_file, group, sample_ID, group_par) = (args.Input, args.group, args.sample ,args.groupname)

par = [abd_file, group, sample_ID, group_par]
if not all(par):
        parser.print_help()
        exit()

threshold  = args.threshold if args.threshold else 0.8
outdir = args.outdir if args.outdir else './'

# 基于重复样品对 OTU 丰度表进行合并处理
def merge_otu(group_file, otu_file, outdir):
    sample = dict()
    sample[''] = '' # 为了输出第一行第一列的空格
    with open(group_file, 'r') as IN:
        for line in IN:
            lst = line.strip('\n').split('\t')
            sample[lst[0]] = lst[8]

    with open(otu_file, 'r') as IN, open(outdir + '/merge_OTU_profile.txt', 'w') as out:
        header = IN.readline().strip('\n').split('\t')
        new_header = [sample[x] for x in header if x in sample]
        out_header = '\t'.join([str(x) for x in sorted(list(set(new_header)))])
        print(out_header, file=out)
        for line in IN:
            lst = line.strip('\n').split('\t')
            outID = lst[0]
            zeroINsample = list()
            counts = defaultdict(int) # value will initialize to 0
            sum = defaultdict(int)
            mean_OTU = dict()
            for x in range(1,len(lst)):
                if lst[x] == '0':
                    zeroINsample.append(new_header[x])
                counts[new_header[x]] += 1
                sum[new_header[x]] += int(lst[x])
            for key in sorted(counts.keys()):
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

# 得到 common OTU 的丰度表，其标准是计算每个分组内在 80% （暂定）样品以上存在的 OTU, 然后将各个分组的 OTU 取并集得到新的 OTU 丰度表
def common_OTU(group_par, sample_ID, threshold, outdir):
    common_OTU_list = list()
    all_groups = group[group_par].unique()
    for item in all_groups:  # 这里是计算三个地点的 common OTU
        lst = group.loc[group[group_par] == item,:][sample_ID].unique() # 计算每个分组的样品
        sub_dt = dt[lst] # 提取每个组的样品
        sample_num = sub_dt.shape[1] #每个组的样品个数
        threshold = sample_num*threshold  # 80% 的阈值
        temp_OTU = sub_dt[(sub_dt != 0).sum(axis = 1) > threshold] #对于每个 OTU, 存在的样品数目大于 80% 的留下来
        common_OTU_list = list(temp_OTU.index) + common_OTU_list  # 累计每个分组的 OTU ，但是会存在重复
    final_OTU = list(set(common_OTU_list)) # 去重
    common_OTU_dt = dt.loc[final_OTU,:]   # 得到 common OTU 表
    outfile = '_'.join(all_groups) + '_commonOTU.xls'
    common_OTU_dt.to_csv(outdir + '/' + outfile, sep ='\t')
    print("Generating the common OTU file: " + outfile)

# 计算某两个组的 core OTU
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
        former_rank = Rank[:len(list(former_lst))] # 依据是 list 的合并是按照顺序来的..
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
otu_file = 'filter_OTU_shared_final.xls'
group_file = 'plant.bms.txt.all.new.name'
merge_otu(group_file, otu_file, outdir)

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

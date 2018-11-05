#! /usr/bin/python3
# 合并暴露期和恢复期不同剂量的，由性别分割，重新生成四个多样性的表格，用于 annova 的差异检验
import pandas as pd
dt = pd.read_table('diversity.txt', header=0)
dt.columns.values[0] = 'SampleID'
df = dt.set_index('SampleID')


# diversity file 
recoveryDf = df.loc[df.index.str.contains('-a'),:]
exposeDf = df.loc[df.index.str.contains('-a') == False,:]
FexposeDf = exposeDf.loc[exposeDf.index.str.contains('F\d', regex=True),:]
MexposeDf = exposeDf.loc[exposeDf.index.str.contains('F\d', regex=True) == False,:]
FrecoveryDf = recoveryDf.loc[recoveryDf.index.str.contains('F\d', regex=True),:]
MrecoveryDf = recoveryDf.loc[recoveryDf.index.str.contains('F\d', regex=True) == False,:]

#group file
exposeGroup = pd.read_table('Sample_information_detail.txt', header=0, index_col=0)
recoveryGroup = pd.read_table('2_Sample_information_detail.xls', header=0, index_col=0)
FexposeGroup = exposeGroup.loc[exposeGroup.index.str.contains('F\d', regex=True),:]
MexposeGroup = exposeGroup.loc[exposeGroup.index.str.contains('F\d', regex=True) == False,:]
FrecoveryGroup = recoveryGroup.loc[recoveryGroup.index.str.contains('F\d', regex=True),:]
MrecoveryGroup = recoveryGroup.loc[recoveryGroup.index.str.contains('F\d', regex=True) == False,:]

# merge file for R analysis
FexposeDiversity = pd.concat([FexposeDf,FexposeGroup], axis=1)
MexposeDiversity = pd.concat([MexposeDf,MexposeGroup], axis=1)
FrecoveryDiversity = pd.concat([FrecoveryDf,FrecoveryGroup], axis=1)
MrecoveryDiversity = pd.concat([MrecoveryDf,MrecoveryGroup], axis=1)

# output
FexposeDiversity.to_csv('FexposeDiversity.txt', sep='\t')
MexposeDiversity.to_csv('MexposeDiversity.txt', sep='\t')
FrecoveryDiversity.to_csv('FrecoveryDiversity.txt', sep='\t')
MrecoveryDiversity.to_csv('MrecoveryDiversity.txt', sep='\t')

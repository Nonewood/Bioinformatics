#! /usr/bin/R
#eg: Rscript adonis.R expose_abd.txt Sample_information_detail.txt Group
library(vegan)
Args <- commandArgs(TRUE)
abd_table = Args[1]  # 丰度文件 expose_abd.txt 
group_table = Args[2] # 分组文件 Sample_information_detail.txt 
var = Args[3] # 需要做检验的组别名字 Group 或者 Sex 之类的

outfile = paste(var,"Adonis.txt", sep="") 
dt = read.table(abd_table, header=T, row.names=1, sep="\t", check.names=F)
group <- read.table(group_table, header=T, check.name = F)
DT <- t(dt)
DT.mat = sqrt(DT)
DT.dist <- vegdist(DT.mat, method="bray")
set.seed(1)
run <- paste("DT.div = adonis2(formula=DT.dist~",var,",data=group,permutations=9999)",sep="")
eval(parse(text = run)) # 首先使用 parse() 函数将字符串转化为表达式(expression),再使用 eval() 函数对表达式求解
write.table(DT.div, file=outfile, quote = F, sep="\t", col.names=NA) #保持第一行第一列的空白位置
#write.table(data.frame("Name"=rownames(DT.div),DT.div,check.names=F), file=outfile, quote = F, sep="\t", row.names=F) #或者给第一行第一列的位置赋值

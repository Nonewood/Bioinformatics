#用来将丰度文件归一化
#! /usr/bin/Rscript
#usage Rscript **.R Rat_10gene_phylum_abundance_profile.xls phylumProfileTable.xls
Args = commandArgs()
input = Args[6]
output = Args[7]
dt = read.table(input,header=T,sep="\t")
rownames(dt) = dt[,1]
df = dt[,-1]
dfNorm = t(t(df)/apply(df,2,sum))*100
write.table(dfNorm,file=output,sep="\t",quote=F,col.names=NA)

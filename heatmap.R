# 根据计算出来的 braycurtis 距离矩阵，画热图，并且进行按照分组进行标识

library('pheatmap')
dt = read.table('braycurtis.txt', header=T)
expose = read.table('expose_diversity', header=T, check.names=FALSE)
expose_group = read.table('Sample_information_detail.txt', header=T, row.names=1, comment.char='', check.names=F) #分组信息，行名需是距离矩阵的列名  
pheatmap(expose, fontsize=9,annotation_col=expose_group, filename='expose_bray.pdf')

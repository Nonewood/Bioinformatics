#! /usr/bin/Rscript 
#eg: Rscript pca.R expose_abd.txt Sample_information_detail.txt CK:E-liquid:Cigarette 67ab57:487eb3:d2382c 
Args <- commandArgs(TRUE)
abd_table = Args[1]  # 丰度文件 expose_abd.txt
group_table = Args[2] # 分组文件 Sample_information_detail.txt
group_list = Args[3] # CK:E-liquid:Cigarette
color_list = Args[4] # 67ab57:487eb3:d2382c
dt = read.table(abd_table, header = T,sep = '\t', row.names = 1, check.names = F)
group = read.table(group_table, header=T, sep="\t", row.names = 1, check.names = F) 
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
legend_list = unlist(strsplit(group_list, ":"))
filename_prefix= gsub(":", "_", group_list)

library(ade4)
library(ggplot2)
#dt_t = t(dt)
dt_t = t(sqrt(dt)) # 原始数据预处理
dt.dudi <- dudi.pca(dt_t,center=TRUE,scale=F,scannf=F,nf=4)
#pca = cbind(dt.dudi$li,group)
merge(dt.dudi$li,group,by="row.names") #原来的合并方式太危险啦
pca$Group = factor(pca$Group, levels=legend_list)
pc1 = round(100*dt.dudi$eig[1]/sum(dt.dudi$eig),2)
pc2 = round(100*dt.dudi$eig[2]/sum(dt.dudi$eig),2)
xlab=paste("PC1(",pc1,"%)",sep="")
ylab=paste("PC2(",pc2,"%)",sep="")
pc = ggplot(pca,aes(x=Axis1,y=Axis2,col=Group,shape = Group)) + 
  geom_point(size = 3) + 
  theme_bw() + 
  scale_color_manual(values = color_var) + 
  labs(x=xlab,y=ylab) + 
  theme(axis.text = element_text(colour = 'black', size = 10), axis.title = element_text(size = 12), 
        panel.background = element_rect(colour = "black", size = 1),panel.grid =element_blank(), legend.key = element_blank(), 
        legend.text = element_text(size = 10), legend.title = element_blank(), legend.position='none', plot.margin = unit(c(0.4, 0.3, 0.1, 0.1 ), 'in'))

## PC1 & PC2 箱线图
library(ggpubr)
pc1_diff = compare_means(Axis1 ~ Group, pca, method = "wilcox.test") ## default wilcox.test
write.table(pc1_diff,file = paste(filename_prefix,"_pc1_Diffresult.txt",sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(pc1_diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) {  # 增加所有差异检验不显著结果的处理
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
    diff_group <- as.character(diff_temp[row, c(2,3)])
    my_comparisons[[row]] = diff_group
}
pc1 = ggplot(pca,aes(x=Group, y=Axis1,colour=Group)) + geom_boxplot()+stat_compare_means(comparisons= my_comparisons ,label = "p.signif", label.y = c(0.02,0.04,0.09) + max(pca$Axis1)) + scale_color_manual(values= color_var) +
  labs(x="", y = "PC1") + scale_y_continuous(limits = c(min(pca$Axis1), max(pca$Axis1) + 0.1)) + 
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.4,0.3, 0, 0), 'in'))
} else {
pc1 = ggplot(pca,aes(x=Group, y=Axis1,colour=Group)) + geom_boxplot() + scale_color_manual(values= color_var) +
  labs(x="", y = "PC1") +
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.4,0.3, 0, 0), 'in'))
  
pc2_diff = compare_means(Axis2 ~ Group, pca, method = "wilcox.test") 
write.table(pc2_diff,file = paste(filename_prefix,"_pc2_Diffresult.txt",sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(pc2_diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) { # 同上
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
    diff_group <- as.character(diff_temp[row, c(2,3)])
    my_comparisons[[row]] = diff_group
}
pc2 = ggplot(pca,aes(x=Group, y=Axis2,colour=Group)) + geom_boxplot()+ stat_compare_means(comparisons= my_comparisons ,label = "p.signif", label.y = c(0.02,0.04,0.09) + max(pca$Axis2)) + scale_color_manual(values= color_var) +
  labs(x="", y = "PC2") + scale_y_continuous(limits = c(min(pca$Axis2), max(pca$Axis2) + 0.1)) + 
  theme(axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0, 0.3, 0.1, 0), 'in'))
} else {
pc2 = ggplot(pca,aes(x=Group, y=Axis2,colour=Group)) + geom_boxplot() + scale_color_manual(values= color_var) +
  labs(x="", y = "PC2") +
  theme(axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0, 0.3, 0.1, 0), 'in'))
#output
pdf(paste(filename_prefix,"_PCA.pdf",sep=""),width=6,height=4)
library(grid)
library("gridBase")
plot.new()
plotlayout <- grid.layout(nrow=2,ncol=3)
vp1 <- viewport(layout.pos.col=c(1,2),layout.pos.row=c(1,2))
vp2 <- viewport(layout.pos.col=3,layout.pos.row=1)
vp3 <- viewport(layout.pos.col=3,layout.pos.row=2)
pushViewport(viewport(layout=plotlayout))
pushViewport(vp1)
par(new=TRUE,fig=gridFIG(),mai=c(1.1,1,0.3,0.2))
print(pc,newpage=FALSE)
popViewport()

pushViewport(vp2)
par(new=TRUE,fig=gridFIG())
print(pc1,newpage=FALSE)
popViewport()

pushViewport(vp3)
par(new=TRUE,fig=gridFIG())
print(pc2,newpage=FALSE)
popViewport()
dev.off()

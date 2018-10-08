#! /usr/bin/R
library(ggpubr)
library("ggplot2")
library("ape")
library("vegan")
Args <- commandArgs(TRUE)
abd_table = Args[1]  # 丰度文件 expose_abd.txt 
group_table = Args[2] # 分组文件 Sample_information_detail.txt 
group_list = Args[3] # Healthy:CASE
color_list = Args[4] # 4daf4a:984ea3
legend_list = unlist(strsplit(group_list, ":"))
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
filename_prefix = gsub(":", "_", group_list)

# plot PCoA 
profile <- t(read.table(abd_table,header=T, row.names=1, sep = "\t", check.name = F))
group <- read.table(group_table, header=T, check.name = F)
beta.dis <- vegdist(profile, method = "bray")
PCOA <- pcoa(beta.dis, correction="none", rn=NULL)
result <- PCOA$values[,"Relative_eig"]
pco1 <- as.numeric(sprintf("%0.3f",result[1]))*100
pco2 <- as.numeric(sprintf("%0.3f",result[2]))*100
pc <- as.data.frame(PCOA$vectors)
pc$SampleID = rownames(profile)
Merge.result <- merge(pc,group,by="SampleID",all=TRUE)
xlab=paste("PCoA1(",pco1,"%)",sep="")
ylab=paste("PCoA2(",pco2,"%)",sep="")
Merge.result$Group = factor(Merge.result$Group, levels=legend_list)
pcoa = ggplot(Merge.result,aes(Axis.1,Axis.2)) +
       geom_point(size=3,aes(color=Group,shape=Group)) + 
       scale_color_manual(values = color_var) + 
       geom_hline(yintercept=0,linetype=4,color="grey") +
       geom_vline(xintercept=0,linetype=4,color="grey") +
       labs(x=xlab,y=ylab) +
       theme_bw() +
       theme(axis.text = element_text(colour = 'black', size = 10), 
		axis.title = element_text(size = 12),
		panel.background = element_rect(colour = "black", size = 1),
		panel.grid =element_blank(), 
		legend.key = element_blank(),
		legend.text = element_text(size = 10), 
		legend.title = element_blank(), legend.position='none', 
		plot.margin = unit(c(0.4, 0.3, 0.1, 0.1 ), 'in'))	

# PCo1 & PCo2
pcoa1_diff = compare_means(Axis.1 ~ Group, Merge.result) ## default wilcox.test 
write.table(pcoa1_diff,file = paste(filename_prefix,"_pcoa1_Diffresult.txt",sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(pcoa1_diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) {   # 增加没有差异检验结果显著的判断
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
    diff_group <- as.character(diff_temp[row, c(2,3)])
    my_comparisons[[row]] = diff_group
}
pcoa1 = ggplot(Merge.result,aes(x=Group, y=Axis.1,colour=Group)) + geom_boxplot()+stat_compare_means(comparisons=my_comparisons, label = "p.signif", label.y = c(0.02,0.04,0.09) + max(Merge.result$Axis.1)) +
  scale_color_manual(values= color_var) + labs(x="", y = "PCoA1") + 
  scale_y_continuous(limits = c(min(Merge.result$Axis.1), max(Merge.result$Axis.1) + 0.1)) + 
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.4,0.3, 0, 0), 'in'))
} else {
pcoa1 = ggplot(Merge.result,aes(x=Group, y=Axis.1,colour=Group)) + geom_boxplot() +
  scale_color_manual(values= color_var) + labs(x="", y = "PCoA1") +
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.4,0.3, 0, 0), 'in'))
}

pcoa2_diff = compare_means(Axis.2 ~ Group, Merge.result) ## default wilcox.test 
write.table(pcoa2_diff,file = paste(filename_prefix,"_pcoa2_Diffresult.txt", sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(pcoa2_diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) {  # 同上
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
    diff_group <- as.character(diff_temp[row, c(2,3)])
    my_comparisons[[row]] = diff_group
}
pcoa2 = ggplot(Merge.result,aes(x=Group, y=Axis.2,colour=Group)) + geom_boxplot()+stat_compare_means(comparisons=my_comparisons, label = "p.signif",label.y = c(0.02,0.04,0.09) + max(Merge.result$Axis.2)) + 
  scale_color_manual(values= color_var) + labs(x="", y = "PCoA2") + 
  scale_y_continuous(limits = c(min(Merge.result$Axis.2), max(Merge.result$Axis.2) + 0.1)) +
  theme(axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0, 0.3, 0.1, 0), 'in'))
} else {
pcoa2 = ggplot(Merge.result,aes(x=Group, y=Axis.2,colour=Group)) + geom_boxplot() +
  scale_color_manual(values= color_var) + labs(x="", y = "PCoA2") +
  theme(axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0, 0.3, 0.1, 0), 'in'))
}
#output
pdf(paste(filename_prefix,"_PCoA.pdf",sep=""),width=6,height=4)
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
print(pcoa,newpage=FALSE)
popViewport()

pushViewport(vp2)
par(new=TRUE,fig=gridFIG())
print(pcoa1,newpage=FALSE)
popViewport()

pushViewport(vp3)
par(new=TRUE,fig=gridFIG())
print(pcoa2,newpage=FALSE)
popViewport()

dev.off()

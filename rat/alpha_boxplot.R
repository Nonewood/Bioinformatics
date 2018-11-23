#! /usr/bin/Rscript
#eg: Rscript alpha_boxplot.R expose_abd.txt Sample_information_detail.txt CK:E-liquid:Cigarette 67ab57:487eb3:d2382c 
library(Rcpp,lib.loc="R_lib")
library(tidyr,lib.loc="R_lib")
library(tidyselect,lib.loc="R_lib")
Args <- commandArgs(TRUE)
input = Args[1]  # alpha diversity file, including number and shannon
group = Args[2]  # F_Sample_information_detail.xls
group_list = Args[3] # E-liquid:Cigarette
color_list = Args[4] # 487eb3:d2382c
abd = read.table(input, header = T,sep = '\t', row.names = 1, check.names = F)
group = read.table(group, header = T,sep = '\t', row.names = 1, check.names = F)
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
legend_list = unlist(strsplit(group_list, ":"))
filename_prefix= gsub(":", "_", group_list)

library(ggplot2)
library(ggpubr,lib.loc="/ifshk7/BC_PS/wangpeng7/R_lib")
dt = cbind(abd,group)
# number boxplot
number_diff = compare_means(number ~ Group, dt, method = "wilcox.test") ## default wilcox.test
write.table(number_diff,file = paste(filename_prefix,"_number_Diffresult.txt",sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(number_diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) {
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
    diff_group <- as.character(diff_temp[row, c(2,3)])
	my_comparisons[[row]] = diff_group
}
number_plot = ggplot(dt,aes(x=Group, y=number,colour=Group)) + geom_boxplot() + stat_compare_means(comparisons= my_comparisons ,label = "p.signif", label.y = c(0.02,0.04,0.09) + max(dt$number)) + scale_color_manual(values= color_var) + labs(x="", y = "Number") + scale_y_continuous(limits = c(min(dt$number), max(dt$number) + 0.1)) + 
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.3,0, 0.1, 0.1), 'in'))
} else {
number_plot = ggplot(dt,aes(x=Group, y=number, colour=Group)) + geom_boxplot() + scale_color_manual(values= color_var) + labs(x="", y = "number") +
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.3,0, 0.1, 0.1), 'in'))
}
# shannon boxplot
shannon_diff = compare_means(shannon ~ Group, dt, method = "wilcox.test") 
write.table(shannon_diff,file = paste(filename_prefix,"_shannon_Diffresult.txt",sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(shannon_diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) {
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
   	diff_group <- as.character(diff_temp[row, c(2,3)])
    my_comparisons[[row]] = diff_group
}
shannon_plot = ggplot(dt,aes(x=Group, y=shannon, colour=Group)) + geom_boxplot()+ stat_compare_means(comparisons= my_comparisons ,label = "p.signif", label.y = c(0.02,0.04,0.09) + max(dt$shannon)) + scale_color_manual(values= color_var) + labs(x="", y = "shannon") + scale_y_continuous(limits = c(min(dt$shannon), max(dt$shannon) + 0.1)) + 
  theme(axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.3, 0.1, 0.1, 0), 'in')) # 上 右  下 左
} else {
shannon_plot = ggplot(dt,aes(x=Group, y=shannon, colour=Group)) + geom_boxplot() + scale_color_manual(values= color_var) + labs(x="", y = "shannon") +
  theme(axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.3, 0.1, 0.1, 0), 'in'))
}
#output
pdf(paste(filename_prefix,"alpha_boxplot.pdf",sep=""),width=6,height=4)
library(grid)
library("gridBase")
plot.new()
plotlayout <- grid.layout(nrow=1,ncol=2)
vp1 <- viewport(layout.pos.col=1,,layout.pos.row=1)
vp2 <- viewport(layout.pos.col=2,layout.pos.row=1)
pushViewport(viewport(layout=plotlayout))
pushViewport(vp1)
#par(new=TRUE,fig=gridFIG(),mai=c(1.1,1,0.3,0.2))
par(new=TRUE,fig=gridFIG())
print(number_plot,newpage=FALSE)
popViewport()

pushViewport(vp2)
par(new=TRUE,fig=gridFIG())
print(shannon_plot,newpage=FALSE)
popViewport()
dev.off()

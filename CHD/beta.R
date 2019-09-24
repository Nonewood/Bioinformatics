# beta, 种, 画 beta 的箱线图，同时标注显著性差异
input = 'intra_distance.txt'  # alpha diversity file, including number and shannon
outdir = './beta/'
group_list =  'sCAD:AMI:sCAD-AMI'  # E-liquid:Cigarette
color_list = 'ea5e74:aa75b3:08519C' # 487eb3:d2382c
dt = read.table(input, header = T,sep = '\t', row.names = 1, check.names = F)
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
legend_list = unlist(strsplit(group_list, ":"))
filename_prefix= gsub(":", "_", group_list)

library(ggplot2)
library(ggpubr)
dt$group = factor(dt$group, levels=legend_list)

diff = compare_means(distance ~ group, dt, method = "wilcox.test") ## default wilcox.test
write.table(diff,file = paste(outdir,filename_prefix,"_Diffresult.txt",sep=""),sep = "\t",quote = F,row.names = F)
diff_temp = as.data.frame(diff)
diff_temp = diff_temp[which(diff_temp$p < 0.05),]
if (nrow(diff_temp) > 0 ) {
my_comparisons = list()
for (row in 1:nrow(diff_temp)) {
    diff_group <- as.character(diff_temp[row, c(2,3)])
	my_comparisons[[row]] = diff_group
}
plot = ggplot(dt,aes(x=group, y=distance)) + 
    geom_violin(aes(fill=group)) + 
    geom_boxplot(width = 0.2) + 
    scale_fill_manual(values= color_var) +
    stat_compare_means(comparisons= my_comparisons ,label = "p.signif", label.y = c(0.04,0.13,0.09) + max(dt$distance)) + scale_color_manual(values= color_var) + 
    labs(x="", y = "Bray distance") + scale_y_continuous(limits = c(min(dt$distance), max(dt$distance)*1.15)) +
    theme(axis.text = element_text(colour = 'black', size = 12),
        #axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 12),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.1,0.1, 0.1, 0.1), 'in'))  #top right bottom left
} else {
plot = ggplot(dt,aes(x=group, y=distance, colour=group)) + geom_boxplot() + scale_color_manual(values= color_var) + labs(x="", y = "bray distance") +
  theme(axis.text = element_text(colour = 'black', size = 8,),
        axis.text.x = element_text(vjust = 0.7, angle = 15),
        axis.title = element_text(size = 10),
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.3,0.3, 0.3, 0.3), 'in'))
}
#output
pdf(paste(outdir,filename_prefix,"_beta_boxplot.pdf",sep=""),width=3.2,height=3)
plot
dev.off()

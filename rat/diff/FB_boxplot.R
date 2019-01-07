library(ggplot2)
library(ggpubr)
Args = commandArgs(TRUE)
fb_table = Args[1] #F_B_ratio_boxplot.txt
group_list = Args[2] #E-liquid:Cigarette
color_list = Args[3] #487eb3:d2382c  颜色的顺序要和上边的组别一致

legend_list = unlist(strsplit(group_list, ":"))
color_var = unlist(strsplit(color_list,":"))
color_var = c(paste("#",color_var,sep=""))
filename_prefix = gsub(":","_", group_list)

dt = read.table(fb_table, header = T, sep ="\t")

#差异计算
FB_diff = compare_means(FB~subgroup, data=dt, group.by = "group")
write.table(FB_diff,file = paste(filename_prefix,"_FB_Diffresult.txt", sep=""),sep = "\t",quote = F,row.names = F)

group_list = c('E-liquid', 'Cigarette')
dt$Subgroup = factor(dt$subgroup, levels=legend_list)
Plot = ggplot(dt,aes(x = group, y = log10(FB))) +
geom_boxplot(aes(color = Subgroup),fatten = 1, lwd = 0.5, outlier.size = 0.5, position = position_dodge(0.9)) +
labs(x ='', y = expression(F/B~ratio~(log['10'])), fill = '', color = '', size = 10 ) +
scale_color_manual(values = color_var) + 
theme(
    axis.text = element_text(colour = 'black', size = 10),
#    axis.text.x = element_text(hjust = 1, angle = 45), #phylum
#   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #genus
#   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 60), #species
    axis.title.y = element_text(size = 10, face = 'bold'),
    axis.line = element_line(size=0.5, colour = "black"),
    legend.position = c(0,0),
    legend.justification = c(0,0),
    legend.key = element_blank(),
    legend.text = element_text(size = 10),
    legend.key.width = unit(0.2, 'in'),
    legend.key.height = unit(0.2, 'in'),
    legend.background = element_blank(),
    panel.background = element_blank(),
    plot.margin = unit(c(0.2, 0.2, 0.1, 0.2), 'in')
) + stat_compare_means(label = "p.signif")

#plot
postscript(paste(filename_prefix,"_FB_boxplot.eps",sep=""), width = 6, height=4)
Plot
dev.off()
#png(paste(filename_prefix,"_FB_boxplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent")
#Plot
#dev.off()

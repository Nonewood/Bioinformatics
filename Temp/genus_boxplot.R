# 输入文件找我要就行了... 
## 属水平
library(ggplot2)
library(dplyr)
dt = read.table('genus_boxplot.txt', header=T)
group_list = "NCA:sCAD:AMI"
color_list = "24af2d:ea5e74:e80211"
#tax_list 这一行需要你提前排好序，我这里前边都是患者（两组疾病）富集的，后边是健康人富集的
tax_list = "Lactobacillus:Megasphaera:Phascolarctobacterium:Pediococcus:Anaeroglobus:Pyramidobacter:Methanosphaera:Desulfotomaculum:Photorhabdus:Sutterella:Elizabethkingia"
legend_list = c(unlist(strsplit(group_list, ":")))
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
tax_order = c(unlist(strsplit(tax_list, ":")))

dt$group_order<-factor(dt$Group, legend_list)
dt$ID_order<-factor(dt$ID, tax_order)
p = ggplot(dt,aes(x = ID_order, y = log10(Abd))) +
    geom_boxplot(aes(fill = factor(group_order)), fatten = 1, lwd = 0.5, outlier.size = 0.5, width = 0.8, position = position_dodge(0.8)) +
   # labs(x ='', y = expression(Relative~abundance~(log['10'])), fill = '', color = '', size = 10 ) +
    labs(x ='', y = "Relative abundance") +
    geom_vline(xintercept=c(9.5), linetype="dotted") +  #这里指定图中的那条虚线..用来区分富集方向
    scale_fill_manual(values = color_var) +
    theme(
        axis.text = element_text(colour = 'black', size = 12),
        #    axis.text.x = element_text(angle = 0),
        #axis.text.x = element_text(hjust = 1, angle = 0), #phylum
        #   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #genus
        axis.text.x = element_text(hjust = 1, face = 'italic', angle = 30), #species
        axis.title.y = element_text(size = 15, face = 'bold'),
        axis.line = element_line(size=0.5, colour = "black"),
        #legend.position = c(0,0),
        legend.justification = c(0,0),
        legend.key = element_blank(),
        legend.text = element_text(size = 10),
        legend.key.width = unit(0.2, 'in'),
        legend.key.height = unit(0.2, 'in'),
        legend.background = element_blank(),
        panel.background = element_blank(),
        plot.margin = unit(c(0.2, 0.2, 0.1, 0.2), 'in')
    )
#postscript(paste("species_boxplot.eps",sep=""), width = 8, height=5)
pdf("genus_boxplot.pdf", width = 8, height=4)
p
dev.off()

#! /usr/bin/Rscript 

library(ggplot2)
library(dplyr)
Args = commandArgs(TRUE)
box_table = Args[1] # boxplot.txt
group_list = Args[2] # EL:Cig
color_list = Args[3] # 487eb3:d2382c
diff_result = Args[4] # EL_Cig.E-liquid-Cigarette.wilcox.test.xls
diff_type = Args[5] # pvalue or qvalue
legend_list = c(unlist(strsplit(group_list, ":")))
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
filename_prefix = gsub(":", "_", group_list)

data = read.table(box_table, header = T, sep = '\t')

# 确定横坐标轴的物种顺序,cig 相当于分组 2 和分组 1，暂时不改动代码
cig_dt = filter(data, Group == legend_list[2])
cig_group = group_by(cig_dt, ID)
cig_summ = summarise(cig_group, cig_median = median(Abd))
el_dt = filter(data, Group == legend_list[1])
el_group = group_by(el_dt, ID)
el_summ = summarise(el_group, el_median = median(Abd))
merge = merge(cig_summ, el_summ, by='ID')
bigger = filter(merge, merge$cig_median > merge$el_median)
less = filter(merge, merge$cig_median < merge$el_median)
x_order = as.character(rbind(bigger[order(bigger$cig_median),]['ID'], less[order(less$cig_median),]['ID'])$ID)
data$x = factor(data$ID, levels=x_order)

data$group<-factor(data$Group, legend_list)
plot = ggplot(data,aes(x = x, y = log10(Abd))) +
geom_boxplot(aes(color = factor(group)), fatten = 1, lwd = 0.5, outlier.size = 0.5, position = position_dodge(0.9)) +
labs(x ='', y = expression(Relative~abundance~(log['10'])), fill = '', color = '', size = 10 ) +
scale_color_manual(values = color_var) +
theme(
	axis.text = element_text(colour = 'black', size = 10),
	axis.text.x = element_text(hjust = 1, angle = 45), #phylum
#	axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #genus
#	axis.text.x = element_text(hjust = 1, face = 'italic', angle = 60), #species
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
)

# 加差异显著的 * 或者 **, 目前只支持 0.05 和 0.01 
df = read.table(diff_result, header=T, sep="\t", check.names = F)
diffID_sig = filter(df, UQ(as.name(diff_type)) < 0.01)$ID
diffID = filter(df, UQ(as.name(diff_type)) > 0.01 & UQ(as.name(diff_type)) < 0.05)$ID
diff_x  = c()
if ( length(diffID) == 0) {
	print(paste("no tax is different for",diff_type,"!",sep=" "))
	q()
}
for (i in 1:length(diffID)) {
    if ( diffID[i] %in% x_order) {
            diff_x = c(diff_x,(which(x_order == diffID[i])))        
    }
}

if (length(diffID_sig != 0) {
	diff_sig_x  = c()
	for (i in 1:length(diffID_sig)) {
   		if ( diffID_sig[i] %in% x_order) {
            diff_sig_x = c(diff_sig_x,(which(x_order == diffID_sig[i])))        
   		}
	}
} 
if (is.null(diff_x) & is.null(diff_sig_x)) {
    print("no tax is different! check your data!")
} else if ( !is.null(diff_x) & is.null(diff_sig_x)) {
    #pdf(paste(filename_prefix,"_boxplot.pdf",sep=""),width=6,height=4)
    png(paste(filename_prefix,"_boxplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent")
	postscript(paste(filename_prefix,"_boxplot.eps",sep=""), width = 6, height=4)
    plot + annotate('text', x = diff_x, y = -2, label='*', size = 5)
#	ggsave(paste(filename_prefix,"_boxplot.eps",sep=""), width = 6, height = 4, units = "in")	
} else if ( is.null(diff_x) & !is.null(diff_sig_x)) {
#    pdf(paste(filename_prefix,"_boxplot.pdf",sep=""),width=6,height=4)
    png(paste(filename_prefix,"_boxplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent")
	postscript(paste(filename_prefix,"_boxplot.eps",sep=""), width = 6, height=4)
    plot + annotate('text', x = diff_sig_x, y = -2, label='**', size = 5)
} else {
#   pdf(paste(filename_prefix,"_boxplot.pdf",sep=""),width=6,height=4)
    png(paste(filename_prefix,"_boxplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent")
	postscript(paste(filename_prefix,"_boxplot.eps",sep=""), width = 6, height=4)
    plot + annotate('text', x = diff_x, y = -2, label='*', size = 5) + annotate('text', x = diff_sig_x, y = -2, label='**', size = 5)
}
dev.off()

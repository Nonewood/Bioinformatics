#根据输入文件，三列，分别是 Group Profile Disease，组别（case&control），数据，疾病组别，画柱状图，并且标显著性差异，小于 0.01 为 ** ，小于 0.05 为 *；
# 有问题请发邮件 liuwangzhang1@gmail.com ~

library("hash")
library("ggplot2")
data <- read.table('Y_temp',header=T,sep="\t")
data$Group <- factor(data$Group, levels=c("Control","Case"))
data$Disease <- factor(data$Disease, levels=c("AS","RA","Gout"))
color = c('#00BFC4','#F8766D')
plot = ggplot(data, aes(x=Disease, y=Profile, fill=Group)) +
        geom_bar(position=position_dodge(), stat="identity") +
        #labs(y="Relative abundance (x 1e-5)",x="Disease",fill="",color="", title=title) +
        scale_fill_manual(values = color) + 
        theme(axis.text.x = element_text(colour="black",size=10),
                axis.text.y = element_text(colour="black",size=10),
                axis.line = element_line(color="black",size=0.5),
                axis.ticks = element_line(color="black",size=0.5),
                axis.title = element_text(color="black",size=10),
                plot.title = element_text(color="black",size=10),
                legend.position="none",
                panel.background = element_blank()
        )

#标显著性差异，根据 P 值大小，< 0.01 两个 * ，< 0.05 但是 > 0.01 一个 * ； 
group = c("AS","RA","Gout") # 顺序需要和 X 轴一致
diff_x  = c()
diff_sig_x  = c()
#pvalue = hash()
for ( i in 1:length(group)){
    subset = data[data$Disease == group[i],]
    p_value = wilcox.test(subset[subset$Group == 'Case',]$Profile, subset[subset$Group == 'Control',]$Profile,)$p.value     
#    .set(pvalue, keys = group[i], values = p_value ) # R 的哈希，记录一下，虽然没有用到
    if (p_value < 0.01){
        diff_sig_x = c(diff_sig_x, i)
        }
    else if (p_value < 0.05) {
        diff_x = c(diff_x, i)
        }
    else {
        next
    }
   }

#输出  注释掉的行用于外接参数和输出文件的情况 
#png
label_y = max(data$Profile)*1.1
if (is.null(diff_x) & is.null(diff_sig_x)) {
    print("no item is different! check your data!")
} else if ( !is.null(diff_x) & is.null(diff_sig_x)) {
    #png(paste(filename_prefix,"_barplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent") #集群
    #png(paste(filename_prefix,"_barplot.png",sep=""), units="in",res=600, width=6, height=4, bg="transparent")
    plot + annotate('text', x = diff_x, y = label_y, label='*', size = 5)
} else if ( is.null(diff_x) & !is.null(diff_sig_x)) {
    #png(paste(filename_prefix,"_barplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent")
    plot + annotate('text', x = diff_sig_x, y = label_y, label='**', size = 5)
} else {
    #png(paste(filename_prefix,"_barplot.png",sep=""),type="cairo",units="in",res=600,width=6,height=4,bg="transparent")
    plot + annotate('text', x = diff_x, y = label_y, label='*', size = 5) + annotate('text', x = diff_sig_x, y =     plot + annotate('text', x = diff_x, y = label_y, label='*', size = 5) + annotate('text', x = label_y, y = -2, label='**', size = 5)
, label='**', size = 5)
}
#dev.off()

#eps
if (is.null(diff_x) & is.null(diff_sig_x)) {
      #print("no item is different! check your data!")
} else if ( !is.null(diff_x) & is.null(diff_sig_x)) {
	#postscript(paste(filename_prefix,"_barplot.eps",sep=""), width = 6, height=4)
    plot + annotate('text', x = diff_x, y = label_y, label='*', size = 5)	
} else if ( is.null(diff_x) & !is.null(diff_sig_x)) {
    
	#postscript(paste(filename_prefix,"_barplot.eps",sep=""), width = 6, height=4)
    plot + annotate('text', x = diff_sig_x, y = label_y, label='**', size = 5)
} else {
	#postscript(paste(filename_prefix,"_barplot.eps",sep=""), width = 6, height=4)
    plot + annotate('text', x = diff_x, y = label_y, label='*', size = 5) + annotate('text', x = diff_sig_x, y = label_y, label='**', size = 5)
}
#dev.off()

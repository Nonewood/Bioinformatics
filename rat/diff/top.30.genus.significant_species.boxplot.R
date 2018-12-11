
library("reshape2",lib.loc="R-3.4.1/library")
library("ggplot2",lib.loc="R-3.4.1/library")
data <- read.table("top.30.genus.log.txt.tt.boxplot.txt",header=T,check.name=F,sep="\t")
data1 <- melt(data)
data1$group <- factor(data1$group,levels=c("Healthy","SCAD","UA","MI"))
color <- c("#4daf4a","#377eb8","#984ea3","#e41a1c")
font_color <- c("#e41a1c","#4daf4a","#984ea3","#000000","#e41a1c","#000000","#4daf4a","#4daf4a","#000000","#4daf4a","#000000","#4daf4a","#4daf4a","#fbb4ae","#4daf4a","#377eb8","#000000","#000000","#000000","#000000","#4daf4a","#000000","#000000","#ccebc5","#e41a1c","#000000","#000000","#4daf4a","#000000","#000000")
plot = ggplot(data1, aes(x=variable, y = value, color = group)) + 
	stat_boxplot(geom="errorbar",size=0.5, width=0.5, position=position_dodge(0.8))+	
	geom_boxplot(outlier.shape = 21, fatten=0.8,size=0.5,outlier.size=0.3,position=position_dodge(0.8)) + 
	scale_color_manual(values= color) + 
	labs(y=expression(Relative~abundance~(log["10"])),x="",fill="",color="") + 
	theme(axis.text.x = element_text(colour=font_color,size=12,face="italic", hjust=1,angle=45),
		axis.text.y = element_text(colour="black",size=10),
		axis.line = element_line(color="black",size=0.5),
		axis.ticks = element_line(color="black",size=0.5),
		legend.position=c(0,0),
		legend.justification=c(0,0),
		legend.key = element_blank(),
		legend.text = element_text(size=10),
		legend.background = element_blank(),
		legend.key.width = unit(0.15, "in"),
		legend.key.height = unit(0.15, "in"),
		panel.background = element_blank(),
		plot.margin = unit(c(0.1, 0.1, 0.1, 0.15), "in")
)

# 加差异显著的 * 或者 **, 目前只支持pvalue 的 0.05 和 0.01, 后边按需修改就好, 利用下边的这段代码，其实可以对任意差异检验的的结果进行显著性标注，只要有上边的箱线图文件和下边的差异检验结果文件
library(dplyr)
diff_result = "Healthy-SCAD-UA-MI.Healthy-SCAD-UA-MI.kruskal.test.xls" # 需要改成外参
x_order = levels(data1$variable)
group_order = c("Healthy","SCAD","UA","MI")     # 改成外参
color_order = c("#4daf4a","#377eb8","#984ea3","#e41a1c") #改成外参数，颜色需要和组别对应
df = read.table(diff_result, header=T, sep="\t", check.names = F)
diffID_sig = filter(df, pvalue < 0.01)$ID
diffID = filter(df, pvalue > 0.01 & pvalue < 0.05)$ID
diff_x  = c()
annotate_color = c() 
for (i in 1:length(diffID)) {
    if ( diffID[i] %in% x_order) {
            diff_x = c(diff_x,(which(x_order == diffID[i])))
			annotate_color = c(annotate_color,color_order[which(group_order == filter(df, ID == diffID[i])$enriched)])
    }
}
diff_sig_x  = c()
annotate_sig_color = c()
for (i in 1:length(diffID_sig)) {
    if ( diffID_sig[i] %in% x_order) {
            diff_sig_x = c(diff_sig_x,(which(x_order == diffID_sig[i])))
			annotate_sig_color = c(annotate_sig_color,color_order[which(group_order == filter(df, ID == diffID_sig[i])$enriched)])
    }
}
pdf("./top.30.genus.log.txt.tt.boxplot.txt.pdf",width=8,height=4,onefile=F)
plot + annotate('text', x = diff_x, y = 0, label='*', color = annotate_color, size = 5) + annotate('text', x = diff_sig_x, y = 0, label='**', color = annotate_sig_color, size = 5)
dev.off()

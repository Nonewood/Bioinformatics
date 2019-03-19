#！/usr/bin/python3
#重现看到的一篇文章的 PCoA 图，可以看干预前后主坐标 1 的变化趋势，还是挺有意思的，输入文件（需要提前处理成一样的格式）在 Data 目录下；
#文章：Links between environment, diet, and the hunter-gatherer microbiome；
# 这是初始版本，接外参,加颜色什么的后边再完善吧..

library("ggplot2")
library("vegan")
library("ape")
dt = read.table('F_phylumProfileTable_PCoA.xls', header = T, row.names=1, sep = "\t", check.name = F)
group = dt %>% select(c('Time','SubjectID'))
group$SampleID = rownames(group)
df = dt %>% select(-c('Time','SubjectID'))
beta.dis <- vegdist(df, method = "bray")
PCOA <- pcoa(beta.dis, correction="none", rn=NULL)
result <- PCOA$values[,"Relative_eig"]
pco1 <- as.numeric(sprintf("%0.3f",result[1]))*100
pco2 <- as.numeric(sprintf("%0.3f",result[2]))*100
xlab=paste("PCoA1(",pco1,"%)",sep="")
ylab=paste("PCoA2(",pco2,"%)",sep="")

pc <- as.data.frame(PCOA$vectors)
axis = pc %>% select(Axis.1, Axis.2)
axis$SampleID = rownames(axis)
plot_dt = merge(axis, group, by='SampleID')

# 生成干预前后带有连线的 PCoA 图
ggplot(plot_dt, aes(Axis.1,Axis.2,group = SubjectID)) + geom_line(color = 'grey') + geom_point(size=3,aes(color=Time))  +
    geom_hline(yintercept=0,linetype=4,color="grey") +
       geom_vline(xintercept=0,linetype=4,color="grey") +
       labs(x=xlab,y=ylab) +
       theme_bw() +
       theme(axis.text = element_text(colour = 'black', size = 10), 
        axis.title = element_text(size = 12),
        panel.background = element_rect(colour = "black", size = 1),
        #panel.grid =element_blank(), 
        legend.key = element_blank(),
        legend.text = element_text(size = 10), 
        #legend.title = element_blank(), legend.position='none', 
        plot.margin = unit(c(0.4, 0.3, 0.1, 0.1 ), 'in'))


#生成主坐标 1 的干预前后变化图
ggplot(plot_dt, aes(Axis.1, SubjectID, group = SubjectID)) + geom_line(color = 'grey') + geom_point(size=3,aes(color=Time))  +
    geom_hline(yintercept=0,linetype=4,color="grey") +
       geom_vline(xintercept=0,linetype=4,color="grey") +
       #labs(x=xlab) +
       theme_bw() +
       theme(axis.text = element_text(colour = 'black', size = 10), 
        axis.title = element_text(size = 12),
        panel.background = element_rect(colour = "black", size = 1),
        #panel.grid =element_blank(), 
        legend.key = element_blank(),
        legend.text = element_text(size = 10), 
        #legend.title = element_blank(), legend.position='none', 
        plot.margin = unit(c(0.4, 0.3, 0.1, 0.1 ), 'in'))

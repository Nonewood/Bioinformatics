library("ggplot2")
library("ape")
library("vegan") 
group <- read.table("Sample_information_detail.txt", header=T, check.name = F, col.names=c('SampleID', 'sex', 'group', 'dose'))
profile <- t(read.table("expose_abd.txt",header=T, sep = "\t", check.name = F))  #原文件在 data 文件夹下
colnames(profile) = profile[1,]
profile = profile[-1,]
test = apply(profile,2,as.numeric)    # 将数据框的字符串格式转化为数值型的矩阵格式，2 表示按照列来处理
rownames(test) = rownames(profile)    
beta.dis <- vegdist(test, method = "bray")
PCOA <- pcoa(beta.dis, correction="none", rn=NULL)
result <- PCOA$values[,"Relative_eig"]
pco1 <- as.numeric(sprintf("%0.3f",result[1]))*100
pco2 <- as.numeric(sprintf("%0.3f",result[2]))*100 
pc <- as.data.frame(PCOA$vectors)
pc$SampleID = rownames(profile)
Merge.result <- merge(pc,group,by="SampleID",all=TRUE)
xlab=paste("PCo1(",pco1,"%)",sep="")
ylab=paste("PCo2(",pco2,"%)",sep="")
ggplot(Merge.result,aes(Axis.1,Axis.2)) +
    geom_point(size=3,aes(color=group,shape=group)) +
    geom_hline(yintercept=0,linetype=4,color="grey") +
    geom_vline(xintercept=0,linetype=4,color="grey") +
    labs(x=xlab,y=ylab) + theme(
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"))
        

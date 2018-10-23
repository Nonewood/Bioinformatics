#! /usr/bin/Rscript
# 计算个体间 SE 函数
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
    library(plyr)

    # New version of length which can handle NA's: if na.rm==T, don't count them
    length2 <- function (x, na.rm=FALSE) {
        if (na.rm) sum(!is.na(x))
        else       length(x)
    }

    # This does the summary. For each group's data frame, return a vector with
    # N, mean, and sd
    datac <- ddply(data, groupvars, .drop=.drop,
      .fun = function(xx, col) {
        c(N    = length2(xx[[col]], na.rm=na.rm),
          mean = mean   (xx[[col]], na.rm=na.rm),
          sd   = sd     (xx[[col]], na.rm=na.rm)
        )
      },
      measurevar
    )

    # Rename the "mean" column    
    datac <- rename(datac, c("mean" = measurevar))

    datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

    # Confidence interval multiplier for standard error
    # Calculate t-statistic for confidence interval: 
    # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
    ciMult <- qt(conf.interval/2 + .5, datac$N-1)
    datac$ci <- datac$se * ciMult

    return(datac)
}



library(ggplot2)
library(dplyr)
library(ggpubr)
library(car)
Args <- commandArgs(TRUE)  
table = Args[1]  #  阿尔法多样性和丰富度文件与分组信息合并以后的  FexposeDiversity.txt
filename_prefix = Args[2] # 分组文件 Sample_information_detail.txt   Fexpose
#group_list = Args[3] # Healthy:CASE

dt = read.table(table, header=T)
dt$Group = ordered(dt$Group, levels=c('CK','E-liquid','Cigarette')) # 标记
theme_set(theme_bw())
# gene number 
dt_summary = summarySE(dt, measurevar="number", groupvars="Group")

number_pc =ggplot(dt_summary, aes(x=Group, y=number, fill=Group)) + 
        geom_bar(position=position_dodge(), stat="identity") + 
        geom_errorbar(aes(ymin=number-se, ymax=number+se),
                  width=.2,                    # Width of the error bars
                  position=position_dodge(10)) +  # 实现条形距离的调整
        scale_fill_manual(values = c("#c8d1a2", "#87d1e0", "#dfb0ce")) +
        labs(x="", y = "Gene Number") + ggtitle(paste(filename_prefix, "gene number barpplot", sep=" ")) + 
        theme(plot.title = element_text(hjust = 0.5),
        axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7),
        axis.title = element_text(size = 10),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.2,0.2, 0.2, 0.2), 'in')) # 上，右，下，左

res.aov = aov(number ~ Group, data = dt)
anova_number = summary(res.aov)
anova_number = data.frame(unclass(anova_number), check.names = FALSE, stringsAsFactors = FALSE)
Tukey_number = TukeyHSD(res.aov)
Tukey_number = data.frame(unclass(Tukey_number), check.names = FALSE, stringsAsFactors = FALSE)

#plot(res.aov, 1) # 方差齐性的图
homogeneity_number  = leveneTest(number ~ Group, data = dt) # 方差齐性检验
homogeneity_number = data.frame(unclass(homogeneity_number), check.names = FALSE, stringsAsFactors = FALSE)
#plot(res.aov, 2)  # 正态分布的图
aov_residuals = residuals(object = res.aov) # Extract the residuals
normality_number = shapiro.test(x = aov_residuals) # 正态分布检验
normality_number  = data.frame(unclass(normality_number), check.names = FALSE, stringsAsFactors = FALSE)

# shannon index 
dt_summary = summarySE(dt, measurevar="shannon", groupvars="Group")
shannon_pc = ggplot(dt_summary, aes(x=Group, y=shannon, fill=Group)) + 
        geom_bar(position=position_dodge(), stat="identity") + 
        geom_errorbar(aes(ymin=shannon-se, ymax=shannon+se),
                  width=.2,                    # Width of the error bars
                  position=position_dodge(10)) +  # 实现条形距离的调整
        scale_fill_manual(values = c("#c8d1a2", "#87d1e0", "#dfb0ce")) +
        labs(x="", y = "shannon index") + ggtitle(paste(filename_prefix, "gene shannon barpplot", sep=" ")) + 
        theme(plot.title = element_text(hjust = 0.5),
            axis.text = element_text(colour = 'black', size = 8),
            axis.text.x = element_text(vjust = 0.7),
            axis.title = element_text(size = 10),
            legend.key = element_blank(), legend.title = element_blank(),
            legend.position='none',plot.margin = unit(c(0.2,0.2, 0.2, 0.2), 'in')) # 上，右，下，左
    
res.aov = aov(shannon ~ Group, data = dt)
anova_shannon = data.frame(unclass(summary(res.aov)), check.names = FALSE, stringsAsFactors = FALSE)
Tukey_shannon = TukeyHSD(res.aov)
Tukey_shannon = data.frame(unclass(TukeyHSD(res.aov)), check.names = FALSE, stringsAsFactors = FALSE)
#plot(res.aov, 1) # 方差齐性的图
homogeneity_shannon = leveneTest(shannon ~ Group, data = dt) # 方差齐性检验
homogeneity = data.frame(unclass(homogeneity_shannon), check.names = FALSE, stringsAsFactors = FALSE)
#plot(res.aov, 2)  # 正态分布的图
aov_residuals = residuals(object = res.aov) # Extract the residuals
normality_shannon = shapiro.test(x = aov_residuals) # 正态分布检验
normality_shannon = data.frame(unclass(normality_shannon), check.names = FALSE, stringsAsFactors = FALSE)

# output
pdf(paste(filename_prefix,"_number_barplot.pdf",sep=""),width=6,height=4)
number_pc
dev.off()

pdf(paste(filename_prefix,"_shannon_barplot.pdf",sep=""),width=6,height=4)
shannon_pc
dev.off()

write.table(anova_number,file = paste(filename_prefix,"_anova_number.txt", sep=""),sep = "\t",quote = F)
write.table(Tukey_number,file = paste(filename_prefix,"_Tukey_number.txt", sep=""),sep = "\t",quote = F)
write.table(homogeneity_number,file = paste(filename_prefix,"_homogeneity_number.txt", sep=""),sep = "\t",quote = F)
write.table(normality_number,file = paste(filename_prefix,"_normality_number.txt", sep=""),sep = "\t",quote = F)

write.table(anova_shannon,file = paste(filename_prefix,"_anova_shannon.txt", sep=""),sep = "\t",quote = F)
write.table(Tukey_shannon,file = paste(filename_prefix,"_Tukey_shannon.txt", sep=""),sep = "\t",quote = F)
write.table(homogeneity_shannon,file = paste(filename_prefix,"_homogeneity_shannon.txt", sep=""),sep = "\t",quote = F)
write.table(normality_shannon,file = paste(filename_prefix,"_normality_shannon.txt", sep=""),sep = "\t",quote = F)


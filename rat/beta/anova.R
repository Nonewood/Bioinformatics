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
library("carData", lib.loc="R_lib")
library("car", lib.loc="R_lib")
Args <- commandArgs(TRUE)
filename = Args[1]  #  阿尔法多样性和丰富度文件与分组信息合并以后的  FexposeDiversity.txt
filename_prefix = Args[2] #   Fexpose
plot_title = Args[3] # genus
order = Args[4] # ACK:EL:Cig
item = Args[5] # distance
group = Args[6] # group

level_order = unlist(strsplit(order,":"))
dt = read.table(filename, header=T)
dt$group = ordered(dt$group, levels=level_order) # 标记
theme_set(theme_bw())

#SE
dt_summary = summarySE(dt, measurevar=item, groupvars=group)

pc =ggplot(dt_summary, aes_string(x=group, y=item, fill=group)) +
        geom_bar(position=position_dodge(), stat="identity") +
        geom_errorbar(aes(ymin=dt_summary[[item]]-se, ymax=dt_summary[[item]]+se), # 太机智了 8..
                  width=.2,                    # Width of the error bars
                  position=position_dodge(10)) +  # 实现条形距离的调整
        scale_fill_manual(values = c("#c8d1a2", "#87d1e0", "#dfb0ce")) +
        labs(x="", y = item) + ggtitle(paste(filename_prefix, plot_title, item,"barpplot", sep=" ")) +
        theme(plot.title = element_text(hjust = 0.5),
        axis.text = element_text(colour = 'black', size = 8),
        axis.text.x = element_text(vjust = 0.7),
        axis.title = element_text(size = 10),
        legend.key = element_blank(), legend.title = element_blank(),
        legend.position='none',plot.margin = unit(c(0.2,0.2, 0.2, 0.2), 'in')) # 上，右，下，左

run = paste("res.aov = aov(",item," ~ ",group,",data=dt)", sep="")
eval(parse(text = run))
anova = summary(res.aov)
anova = data.frame(unclass(anova), check.names = FALSE, stringsAsFactors = FALSE)
Tukey = TukeyHSD(res.aov)
Tukey = data.frame(unclass(Tukey), check.names = FALSE, stringsAsFactors = FALSE)
#plot(res.aov, 1) # 方差齐性的图
run = paste("homogeneity = leveneTest(",item," ~ ",group,",data=dt)", sep="")
eval(parse(text = run))
#homogeneity  = leveneTest(item ~ group, data = dt) # 方差齐性检验
homogeneity = data.frame(unclass(homogeneity), check.names = FALSE, stringsAsFactors = FALSE)
#plot(res.aov, 2)  # 正态分布的图
aov_residuals = residuals(object = res.aov) # Extract the residuals
normality = shapiro.test(x = aov_residuals) # 正态分布检验
normality  = data.frame(unclass(normality), check.names = FALSE, stringsAsFactors = FALSE)

# output
pdf(paste(filename_prefix,"_",item,"_barplot.pdf",sep=""),width=6,height=4)
pc
dev.off()
write.table(anova,file = paste(filename_prefix,"_anova_",item,".txt", sep=""),sep = "\t",quote = F,col.names=NA)
write.table(Tukey,file = paste(filename_prefix,"_Tukey_",item,".txt", sep=""),sep = "\t",quote = F,col.names=NA)
write.table(homogeneity,file = paste(filename_prefix,"_homogeneity_",item,".txt", sep=""),sep = "\t",quote = F,col.names=NA)
write.table(normality,file = paste(filename_prefix,"_normality_",item,".txt", sep=""),sep = "\t",quote = F,col.names=NA)

使用 pROC 画表型数据的多条 ROC
library(pROC) # install with install.packages("pROC")
library(randomForest) 
library(dplyr)
dt = read.table('Phenotype.xls', sep = '\t', head = T, row.names = 1) # 表型文件；

temp = rownames(dt)
dt = dt %>% mutate(Disease = ifelse(Group == 'NCA', 0, 1)) # 增加一列，将组别信息转化为 0，1
rownames(dt)= temp
head(dt)

#par(mar=c(3, 3, 3, 2))
pdf("phenotype_roc.pdf",width=3, height=3, onefile=FALSE)  # 因为表型有不少缺失值，剔除
sub_dt = dt[complete.cases(dt['TC']),]
rf.model <- randomForest(factor(sub_dt$Disease) ~ sub_dt$TC)
roc(sub_dt$Disease, rf.model$votes[,1], plot=TRUE, legacy.axes=TRUE, xlab="1 - specificity", ylab="sensitivity", col="#3fadaf", lwd=1, print.auc=F, print.auc.cex=0.5, cex.lab=0.7, cex.axis = 0.7, tck = -0.02, mgp=c(1,0.2,0)) #调整画图的参数；
#p = roc(sub_dt$Disease, rf.model$votes[,1], plot=TRUE, legacy.axes=TRUE, xlab="1 - specificity", ylab="sensitivity", col="#3fadaf", lwd=1, print.auc=F, print.auc.cex=0.5, cex.lab=0.7, cex.axis = 0.7, tck = -0.02, mgp=c(1,0.2,0)) #调整画图的参数；
#print(p$auc) # 这样可以直接输出 auc 值；

sub_dt = dt[complete.cases(dt['LDLC']),]
rf.model <- randomForest(factor(sub_dt$Disease) ~ sub_dt$LDLC)
plot.roc(sub_dt$Disease, rf.model$votes[,1] , col="#ca5477", lwd=1, print.auc=F, print.auc.cex=0.5, add=TRUE, print.auc.y=0.45) # 所有的 print.auc 设置为否，因为出来不好看，后边在 legend 需要自定义

sub_dt = dt[complete.cases(dt['cTnI']),]
rf.model <- randomForest(factor(sub_dt$Disease) ~ sub_dt$cTnI)
plot.roc(sub_dt$Disease, rf.model$votes[,1], col="#76a44a", lwd=1, print.auc=F, add=TRUE, print.auc.cex=0.5, print.auc.y=0.4)

sub_dt = dt[complete.cases(dt['CKMB']),]
rf.model <- randomForest(factor(sub_dt$Disease) ~ sub_dt$CKMB)
plot.roc(sub_dt$Disease, rf.model$votes[,1], col="#946ec6", lwd=1, print.auc=F, add=TRUE, print.auc.cex=0.5,  print.auc.y=0.35)

sub_dt = dt[complete.cases(dt['MYO']),]
rf.model <- randomForest(factor(sub_dt$Disease) ~ sub_dt$MYO)
plot.roc(sub_dt$Disease, rf.model$votes[,1], col="#c57b3d", lwd=1, print.auc=F, add=TRUE, print.auc.cex=0.5, print.auc.y=0.3)

legend("bottomright", legend=c("TC_AUC: 0.609", "LDLC_AUC: 0.616", "CKMB_AUC: 0.671", "MYO_AUC: 0.842", "cTnI_AUC: 0.866"), col=c("#3fadaf", "#ca5477", "#946ec6", "#c57b3d", "#76a44a"), lwd=1,  cex=0.31, pt.cex = 1, bty = "n")  # legend 以及参数
dev.off()

# 这里手动输入 图例元素 还是有点儿笨拙，待优化，时间关系，后边再说，完成任务最重要；


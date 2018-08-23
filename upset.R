library(UpSetR，lib.loc = "/installpath/R_lib") #指定加载包的路径
pdf("upset.pdf", width=8,height=6, onefile = FALSE) #输出到 pdf 文件，并且取消第一页的空白页
gene <- read.csv('Data/upset.csv', header = T, sep = '\t') 
upset(gene, order.by = "degree", mb.ratio = c(0.70, 0.30))
dev.off()
# 就这么简单，成图..

library(UpSetR)
gene <- read.csv('Data/upset.csv', header = T, sep = '\t')
upset(gene, order.by = "degree", mb.ratio = c(0.70, 0.30))
# 就这么简单，成图..

library(ggplot2)
exp_div = read.table('exp_div.txt', header=T, row.names=1)
ggplot(exp_div, aes(x=factor(exp_div$Group, level=c('CK','Cigarette','E-liquid')), y=exp_div$shannon, fill = Group)) + geom_boxplot() + labs(x="",y="shannon index") + theme(
    axis.text = element_text(colour = 'black', size = 10),
    axis.title = element_text(size = 10, face = 'bold'),
    axis.line = element_line(size=0.5, colour = "black"),
    legend.position = c(0,0),
    legend.justification = c(0,0),
    legend.key = element_blank(),
    legend.text = element_text(size = 10),
    legend.key.width = unit(0.2, 'in'),
    legend.key.height = unit(0.2, 'in'),
    legend.background = element_blank(),
    panel.background = element_blank(),
    plot.margin = unit(c(0.2, 0.2, 0.1, 0.2), 'in'))

#差异检验
ck_sha = filter(exp_div, Group=='CK')$shannon
cig_sha = filter(exp_div, Group=='Cigarette')$shannon
el_sha = filter(exp_div, Group=='E-liquid')$shannon
wilcox.test(ck_sha,cig_sha)$p.value
wilcox.test(ck_sha,el_sha)$p.value
wilcox.test(cig_sha,el_sha)$p.value

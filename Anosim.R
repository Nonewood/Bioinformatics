library(ggplot2)
library(vegan)
data(iris)
dt = subset(iris, select = -Species)
iris.dist = vegdist(dt)
m = monoMDS(iris.dist)
dat = as.data.frame(m$points)
dat$group =  iris$Species
ggplot(dat, aes(MDS1,MDS2, col=group, shape=group)) + geom_point()  +
        theme(
        panel.background = element_blank(),
        axis.line = element_line(size=0.5, colour = "black"))
iris.anno = anosim(iris.dist, iris$Species, permutations = 999)
iris.anno
#Call:
#anosim(x = iris.dist, grouping = iris$Species, permutations = 999) 
#Dissimilarity: bray 

#ANOSIM statistic R: 0.8576     R=0，表示组间没有差异，说明实验组和对照组之间没有差异；R> 0，表示组间差异大于组内差异，说明实验组和对照组之间存在差异
#      Significance: 0.001  当然，如果我们得出R值大于0， 还不足以说明实验组和对照组之间存在差异，我们还缺少一个p值，此时常用的检验方法是Permutation Test (置换检验)

#Permutation: free
#Number of permutations: 999

plot(iris.anno)

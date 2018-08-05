# 置换检验的一个例子，来自参考链接
a<-c(24,43,58,67,61,44,67,49,59,52,62,50,42,43,65,26,33,41,19,54,42,20,17,60,37,42,55,28) #生成 28 个数据
group<-factor(c(rep("A",12),rep("B",16))) # A,B 分别重复 12,16 次 
data<-data.frame(group,a)  #合并成数据框
find.mean<-function(x){    #计算 A,B 标签对应数据的均值差
mean(x[group=="A",2])-mean(x[group=="B",2])  
}
mean_obs = find.mean(data) #计算实际数据的均值差
results<-replicate(999,find.mean(data.frame(group,sample(data[,2]))))    #随机打乱 28 个数据，赋予标签 A,B，计算对应的均值差，重复 999 词
p.value<-length(results[results>mean(data[group=="A",2])-mean(data[group=="B",2])])/1000 #统计大于实际均值差的均值比例；
hist(results,breaks=20,prob=TRUE)  #画图
lines(density(results))   #加拟合线
points(mean_obs, p.value, pch=16)  # 画出实际均值差为横坐标，对应 P 值为纵坐标的实心点
  

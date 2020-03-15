# /user/bin/Rscript 
# 对离散型变量进行差异检验，理论频数小于 5 用 fisher ， 否则用卡方检验； 输出两种文件，一种是表型每种分类的的个数以及百分比，另外一种是差异检验的结果，暂且不用多重校正。
library(dplyr)
library(data.table)
dt = read.table('../Samle_Information_categorical.xls', sep = '\t', header = T)
group = 'NS:FS:CS' #the colname of group is 'Group'
group_list = unlist(strsplit(group, ":"))
indice_index = 3 #表型开始的列的位置，从 1 开始

fileConn<-file("diff_results.xls",'w')
head = paste('Characteristic', 'P value', 'Method', sep ='\t')
writeLines(head, fileConn)

# 计算连续变量的 sd 和 mean ... 但是我目前不需要这个...
#temp = dt[c('Group', 'Age')]
#ag = aggregate(. ~ Group, temp, function(x) c(mean = round(mean(x),2), sd = round(sd(x),2)))
#ag_flat <- do.call("data.frame", ag) # flatten

for (index in indice_index:ncol(dt)){
    indice = colnames(dt)[index]
	sub_dt = dt[c('Group',indice)] # 提取

	freq = sub_dt %>%
    group_by(Group, eval(parse(text = indice))) %>%  # 将变量转化为内置变量（大概这么叫吧）
    summarise(n = n()) %>%                           # 天呐这个功能太好用了...
    mutate(freq = round(n / sum(n)*100,2)) %>%       #另一个常见的操作是添加新的列。这就是mutate()函数的工作了。
    mutate(item = paste(n,'(', freq, ')', sep = ''))
	colnames(freq)[2] = indice

#freq
	need = freq[c('Group',indice,'item')]
#need
	dt_cast = dcast(need, eval(parse(text = indice))~Group, value.var='item', fill=0) #太牛批了
	colnames(dt_cast)[1] = indice
	dt_cast = dt_cast[c(indice,group_list)]
#dt_cast
	write.table(dt_cast, file = paste(indice, "information.xls", sep = "_"),sep="\t",quote = F, row.names = F)

#计算 P 值
	ctable = table(sub_dt)

	if (any(ctable < 5)){
    	p = fisher.test(ctable, simulate.p.value = TRUE, B = 1e6)$p.value
	    line = paste(indice, p, 'fisher', sep ='\t')
	    writeLines(line, fileConn)
	} else {
    	p = chisq.test(ctable)$p.value
    	line = paste(indice, p,'chisq', sep ='\t')
		print(indice)
    	writeLines(line, fileConn)
    }
}
close(fileConn)

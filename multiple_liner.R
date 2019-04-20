# /usr/bin/Rscript
#数据在本地，利用多元线性回归校正混在因子，得出相应的 P 值，待完善....
dt = read.table('SamplingTime_BMI_gout.tsv', header = T)
end = length(colnames(dt))
para = c("SamplingTime","BMI")
outfile = paste(c(para,"lm.txt"), collapse="_")
head = "Tax\tFactor\tEstimate\tStd. Error\tt value\tP_value"
cat(head, file=outfile, sep="\n")
start = length(para) + 2
for(i in start:end){
    tax = colnames(dt)[i]
    temp_rowname = c(para,tax)
    temp_dt = dt[temp_rowname]
    run = paste("model = lm(", tax, " ~., data=temp_dt)", sep="")
    eval(parse(text = run)) #再一次用到了将变量转化为表达式的问题。。。特别容易忘记啊...
    dt_p = as.data.frame(summary(model)$coefficient)
    dt_res = dt_p[-1,] # 去掉截距，感觉暂时用不到，其他元素保留输出
    colnames(dt_res)[length(colnames(dt_res))] = 'P_value'
    part_head = paste(colnames(dt_res),collapse = "\t") # 连接向量
    #head = paste('Tax\tFactor',part_head, sep="\t")
    for(i in(1:length(rownames(dt_res)))){
        sub_line = paste(dt_res[rownames(dt_res)[i],], collapse="\t")
        line = paste(tax,rownames(dt_res)[i], sub_line,sep="\t")
        cat(line, file = outfile, sep="\n", append=T)
    }
}
# 先处理成这样子吧，后续的按照表型因子分开以及 P 值的校正，后边再处理

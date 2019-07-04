#! /usr/bin/Rscript
dt = read.table('../SamplingTime_BMI_gout.tsv', header = T)
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
    eval(parse(text = run))
    dt_p = as.data.frame(summary(model)$coefficient)
    dt_res = dt_p[-1,] #delete the intercept
    colnames(dt_res)[length(colnames(dt_res))] = 'P_value'
    part_head = paste(colnames(dt_res),collapse = "\t") # join the vector by "\t"
    #head = paste('Tax\tFactor',part_head, sep="\t")
    for(i in(1:length(rownames(dt_res)))){
        sub_line = paste(dt_res[rownames(dt_res)[i],], collapse="\t")
        line = paste(tax,rownames(dt_res)[i], sub_line,sep="\t")
        cat(line, file = outfile, sep="\n", append=T)
    }
}
# to be continued, like add parameters, split the result file and adjusted the p value

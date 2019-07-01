#! /usr/bin/Rscript  #写得挺烂的。。。有时间改改。。
Args <- commandArgs(TRUE)
abundance_table = Args[1] # should begin with "SampleID", to be continued
group_table = Args[2] # group informational should be 'Group', should begin with "#SampleID"
indice = Args[3]  # Age:BMI:SUA
group = Args[4] #T0:Control
prefix = Args[5] #
outdir = Args[6]
indice_list = unlist(strsplit(indice,":"))
group_list = unlist(strsplit(group,":"))
filename_prefix= gsub(":", "_", indice)
filename = paste(paste(prefix,filename_prefix, sep="_"),"tsv", sep=".")
outfile = paste(outdir,filename,sep="/")
info = read.table(group_table,header = T,sep = "\t",comment.char = "", check.names =F)
#index = info$SamplingTime %in% group_list #gout
index = info$Group %in% group_list
infoSub = info[index,] #select lines contain "T0" and "Control"
indices = c("#SampleID",indice_list)
infoSub_indice = subset(infoSub,select = indices)# select data according to colnames
colnames(infoSub_indice)[1] = "SampleID"
## delete lines contain "NA"
delSample = as.character(infoSub_indice[!complete.cases(infoSub_indice),]$SampleID) # need delete sampleID
needInfo = infoSub_indice[!infoSub_indice$SampleID %in% delSample,]

profile = read.table(abundance_table,header = T,sep = "\t")
profile_t = t(profile)
colnames(profile_t) = profile_t[1,]
profile_t = profile_t[-1,]
profileDel = profile_t[rownames(profile_t) %in% needInfo[,1],]
mode(profileDel) <- "numeric"
profileNorm = profileDel
rownames(needInfo) = needInfo$SampleID
merge.tsv = merge(needInfo,profileNorm, by = 'row.names', all = T)
#print(merge.tsv)
merge.tsv = merge.tsv[,-1]
write.table(merge.tsv,file = outfile ,sep = "\t",quote = F,row.names = F)

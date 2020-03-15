library("MatchIt")

# 获取 FS 匹配的 CS ，之所以选 FS 为「对照」组是因为它的样品数目最少，可以可其他两组最大化配对；
dt = read.table('Samle_Information.xls', sep = '\t', row.names = 1, header = T)
dt = dt[c('Group','Age', 'BMI', 'Ethnicity','Gender','Married','Breakfast','Diet','Vegetable','Fruit','Meat','Dairy.products','Coarse.grain','Eggs','Drinking','Antibiotic','Mouthwash','Oral.ulcer','Bleeding.gums','Dental.caries','Pulpitis','Periodontitis','Constipation','Insomnia','Cold','Sore.throat')]  #对所有这些因素进行综合评分挑选样品
dt = dt[dt['Group'] != 'NS',]
temp = rownames(dt)
dt = dt %>% mutate(Group = ifelse(Group == 'FS', 1, 0))
rownames(dt)= temp
m = matchit(Group ~ Age + BMI +  Ethnicity + Gender + Married + Breakfast + Diet + Vegetable + Fruit + Meat + Dairy.products + Coarse.grain + Eggs + Drinking + Antibiotic + Mouthwash + Oral.ulcer + Bleeding.gums + Dental.caries + Pulpitis + Periodontitis + Constipation + Insomnia + Cold + Sore.throat ,data = dt,method ="nearest", ratio =1) 
matched <- match.data(m)
cs_id = rownames(matched[matched['Group'] == 0,])

# 获取 FS 匹配的 NS
dt = read.table('Samle_Information.xls', sep = '\t', row.names = 1, header = T)
dt = dt[c('Group','Age', 'BMI', 'Ethnicity','Gender','Married','Breakfast','Diet','Vegetable','Fruit','Meat','Dairy.products','Coarse.grain','Eggs','Drinking','Antibiotic','Mouthwash','Oral.ulcer','Bleeding.gums','Dental.caries','Pulpitis','Periodontitis','Constipation','Insomnia','Cold','Sore.throat')]
dt = dt[dt['Group'] != 'CS',]
temp = rownames(dt)
dt = dt %>% mutate(Group = ifelse(Group == 'FS', 1, 0))
rownames(dt)= temp
m = matchit(Group ~ Age + BMI +  Ethnicity + Gender + Married + Breakfast + Diet + Vegetable + Fruit + Meat + Dairy.products + Coarse.grain + Eggs + Drinking + Antibiotic + Mouthwash + Oral.ulcer + Bleeding.gums + Dental.caries + Pulpitis + Periodontitis + Constipation + Insomnia + Cold + Sore.throat, data = dt,method ="nearest", ratio =1)
matched <- match.data(m)
ns_id = rownames(matched[matched['Group'] == 0,])
fs_id = rownames(dt[dt['Group'] == '1',])

dt = read.table('Samle_Information.xls', sep = '\t', row.names = 1, header = T)
write.table(dt[c(fs_id,cs_id,ns_id),], file = 'matched_Samle_Information.xls', sep = "\t",quote = F) #输出配对后的表型信息表

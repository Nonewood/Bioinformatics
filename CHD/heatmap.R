# zscore 热图

## 门
library(pheatmap)
dt = read.table("zscore_phylum.txt", header=TRUE, sep="\t", comment.char = "", check.names = T, row.names=1)
col_anno = read.table('annotation_col.txt', header=T, row.names = 1, sep="\t", check.names = 'F')
ann_colors = list("NCA vs sCAD" = c( No.sig = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"),
                  "NCA vs AMI" = c( No.sig = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"),
                  "sCAD vs AMI" = c( No.sig   = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"))
pheatmap(dt, cluster_rows = F, color = colorRampPalette(c("navy", "white", "firebrick3"))(50), annotation_col=col_anno, annotation_colors = ann_colors,fontsize = 8, cellheight = 20, cellwidth = 20, filename = 'phylum_zscore.pdf', width = 10, height = 8)


#种
library(pheatmap)
dt = read.table("zscore_species.txt", header=TRUE, sep="\t", comment.char = "", check.names = T, row.names=1)
col_anno = read.table('species_annotation_col.txt', header=T, row.names = 1, sep="\t", check.names = 'F')
ann_colors = list("NCA vs sCAD" = c( No.sig = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"),
                  "NCA vs AMI" = c( No.sig = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"),
                  "sCAD vs AMI" = c( No.sig   = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"))
pheatmap(dt, cluster_rows = F, color = colorRampPalette(c("navy", "white", "firebrick3"))(50), annotation_col=col_anno, annotation_colors = ann_colors,fontsize = 8, cellheight = 8, cellwidth = 8, filename = 'species_zscore.pdf', width = 10, height = 8)

#指定五个物种的 zscore

dt = read.table("zscore_five_species.txt", header=TRUE, sep="\t", comment.char = "", check.names = T, row.names=1)
col_anno = read.table('five_species_annotation_col.txt', header=T, row.names = 1, sep="\t", check.names = 'F')
ann_colors = list("NCA vs sCAD" = c( No.sig = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"),
                  "NCA vs AMI" = c( No.sig = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"),
                  "sCAD vs AMI" = c( No.sig   = "#ffffff", "P<0.05" = "#9bc67a" , "P<0.01" = "#009845"))
pheatmap(dt, cluster_rows = F, color = colorRampPalette(c("navy", "white", "firebrick3"))(50), annotation_col=col_anno, annotation_colors = ann_colors,fontsize = 8, cellheight = 20, cellwidth = 20, filename = 'five_species_zscore.pdf', width = 10, height = 8)


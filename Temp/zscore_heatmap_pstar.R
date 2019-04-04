##绘制 zscore 的热图，并且用星星表示显著性差异，使用的数据是已经发表的文章的数据，涉及的文件我会放到同级的 Data 的目录下；
#蔡军门水平 zscore
library('ComplexHeatmap')
library(png)
#这个输入文件需要提前处理好，根据丰度文件
dt = read.table("CJ_zscore_phylum.txt", header=TRUE, sep="\t", comment.char = "", check.names = F, row.names=1)

#读取注释文件，这个文件也是需要提前处理好，用来表示显著性差异的
temp = read.table('CJ_phylum_annotation_col.txt', sep = "\t", header = TRUE, row.names = 1, comment.char = "", check.names = F)

#首先画热图，需要得到聚类的顺序
p = Heatmap(dt,rect_gp = gpar(col = "grey50", lwd = 1), name = "", heatmap_legend_param = list(border = "grey60"), cluster_rows = F, cluster_columns = T,show_row_names = T)
temp_anno = temp[colnames(dt)[column_order(p)],]

#注释文件的图片路径，这个脚本实际上是把星星的图片，绘制在了热图下边，所以需要提供图片文件，在 Data 目录下。类推的话，如果想画其他图片也是可以的，
p_png = "Data/218-star-full.png"
lessp_png = "Data/leessp.png"
no_sig_png = "Data/no_sig.png"

#将注释文件的字符串转变为变量
Control_vs_CHD = as.character(lapply(as.character(temp_anno$`Control vs CHD`), function(x) eval(parse(text = x))))
Control_vs_STEMI = as.character(lapply(as.character(temp_anno$`Control vs STEMI`), function(x) eval(parse(text = x))))
CHD_vs_STEMI = as.character(lapply(as.character(temp_anno$`CHD vs STEMI`), function(x) eval(parse(text = x))))

#生成热图的注释
ha = HeatmapAnnotation(
     "Control vs CHD" = anno_image(Control_vs_CHD, border = F, height = unit(7,"mm"), space = unit(7, "mm")),
     "Control vs STEMI" = anno_image(Control_vs_STEMI,border = F, height = unit(7,"mm"), space = unit(7, "mm")),
     "CHD vs STEMI" = anno_image(CHD_vs_STEMI,border = F, height = unit(7,"mm"), space = unit(7, "mm")),
      annotation_name_gp = gpar(fontsize = 20) # 调节大小
    ## 上边是门水平的脚本，如果画属或者种的话，需要调节图片的参数
    #"NCA vs sCAD" = anno_image(NCA_vs_sCAD, border = F, height = unit(4,"mm"), space = unit(4, "mm")),  #需要通过调节参数控制图片大小
    #"NCA vs AMI" = anno_image(NCA_vs_AMI,border = F,height = unit(4,"mm"),space = unit(4, "mm")), 
    #"sCAD vs AMI" = anno_image(sCAD_vs_AMI,border = F,height = unit(4,"mm"), space = unit(4, "mm"))
)

pdf("phylum_heatmap.pdf", height = 8, width =8)
Heatmap(dt, color = c("navy", "white", "firebrick3"), rect_gp = gpar(col = "grey50", lwd = 1), name = "", heatmap_legend_param = list(border = "grey50"), cluster_rows = F, cluster_columns = T,show_row_names = T, bottom_annotation = ha, width = unit(2*ncol(dt), "cm"), height = unit(2*nrow(dt), "cm"), row_names_gp = gpar(fontsize = 20), column_names_gp = gpar(fontsize = 20))
##这个也是，有时候需要调节 cell ，字体大小什么的，不同水平的都要针对性的调整
#Heatmap(dt, color = c("navy", "white", "firebrick3"), rect_gp = gpar(col = "grey50", lwd = 1), name = "", heatmap_legend_param = list(border = "grey50"), cluster_rows = F, cluster_columns = T,show_row_names = T, bottom_annotation = ha, width = unit(4*ncol(dt), "mm"), height = unit(4*nrow(dt), "mm"), row_names_gp = gpar(fontsize = 10), column_names_gp = gpar(fontsize = 10), heatmap_height = 10, heatmap_width = 10)
dev.off()          

# Bioinformatics

***
20180626  diversity.py  
用 python3 的 pandas 计算了基于丰度表的丰富度和 shannon 物种多样性指数,相比较之前写脚本遍历计算，基于数据框的运算爽很多. 命名为之 diversity.py,目前只能计算两个,以后看情况再加咯.

***
20180627  2017年影响因子 20180626.xlsx  
增加了刚出的截止至 2017 年杂志的影响因子(Journal Citation Reports).

***
20180710  NCBIscrapy.py  
利用 python3 的爬虫帮别人爬取 NCBI 网站上的一些东西，比较简单，留作记录.

***
20180714  geneInsample.py  
得到基因丰度表以后，计算基因在样本中的存在情况，如至少在 10% 的样本存在的基因有多少，20%，30%... 以此类推.
并且按照需要输出低于某一阈值的基因 ID, 用来后续分析的过滤，如在少于 10% 样品中存在的基因 ID.  

***
20180714  numToid.py  
接上一步，过滤出来至少在 10% 样品中存在的基因编号后，需要得到相应的基因 ID (因为之前基因长度文件配置的缘故，现在要替换回来).  
没有用字典，试着用 pandas 的 concat 功能, 将两个数据集按照行索引取交集合并，提取编号和与之对应的 ID, 单独输出到文件.  

***
20180718 补充 geneInsample.py  
修改 geneInsample.py, 使得脚本能输出高于某一阈值的基因丰度表，如大于 10% 样本中存在的所有基因的丰度表，用于物种丰度表的表征.  

***
20180718  
profileNorm.R: 将上一步生成的物种丰度文件（用别人的脚本生成）归一化处理，即每列加和数字等于 1.  
plotIdGenerate.py: 统计丰度表中，所有大于 1（1%）的物种的 ID, 画柱状图时, 需要把在所有样品中小于 1% 的物种合并为 others, 想了半天才想起来这个脚本的功能，必须得做好日志文件呀.  

***
20180725  
small_script.py 统计基因注释文件里，注释到门，属，种水平的基因个各有多少，全程用了 pandas, 用到了 pandas 的切分某列，将 None 替换为 Nan, 按照列计数，还有 unique 功能.  

***
20180726  
braycurtis.py 根据丰度文件计算 bray-curtis 距离，生成样品之间的距离矩阵，没有找到 python3 比较便捷的方法，所以自己用笨的办法写了脚本, 待完善;

***
20180730  
SplitbyRownames.py 根据行名包含哪些字符将数据框分开，R 对应的功能没有找到，但是 pyhton3 有，R 目前只知道根据行名筛选的（select）功能，待完善；  

***
20180731  
heatmap.R 根据计算出来的 braycurtis 距离矩阵，画热图，并且进行按照分组进行标识;  
参考链接：[R语言绘制热图——pheatmap - CSDN博客](https://blog.csdn.net/sinat_38163598/article/details/72770404)  

boxplot.R 箱线图与差异检验（wilcox.test）  

***  
20180805  
permutation.R 置换检验, Permutation test 置换检验是 Fisher于20世纪30年代提出的一种基于大量计算（computationally intensive），利用样本数据的全（或随机）排列，进行统计推断的方法，因其对总体分布自由，应用较为广泛，特别适用于总体分布未知的小样本资料， 以及某些难以用常规方法分析资料的假设检验问题。在具体使用上它和Bootstrap Methods类似，通过对样本进行顺序上的置换，重新计算统计检验量，构造经验分布，然后在此基础上求出P-value进行推断，简单记录;    
参考链接：[置换检验（R语言实现）](https://blog.csdn.net/zhouyijun888/article/details/69524200)  





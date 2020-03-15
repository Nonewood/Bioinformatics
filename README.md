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

***
20180815
PCoA.R 看了好长时间的文献后，终于可以写脚本了，写好了 PCoA 分析，这个貌似网上不怎么能找得到比较好的教程，所以花费时间比较久；  
新建了一个 Data 文件夹，用来放置脚本处理的源文件，方便以后的重现，毕竟脚本多了可能记不起来了；  
还是写脚本比较舒服；  

***
20180816  
anosim.R  anosim 分析，ANOSIM (analysis ofsimilarities) 分析，也叫相似性分析，主要是用于分析高维度数据组间，相似性的统计方法，比如我们经常做完PCoA、NMDS等降维分析的时候(如下图)，看着组,间样本是区分开的，但是缺少一个P值，说明这种差异到底是否显著。  
参考链接：[什么是ANOSIM分析](http://www.360doc.com/content/18/0113/21/33459258_721682039.shtml)

***
20180823  
upset.R 花了点儿时间摸索了个软件，可以代替 venn 图查看多个数据集的交集情况, [软件参考链接](http://caleydo.org/tools/upset/) 目前实现的功能还比较简单, 因为暂且不需要多复杂。  

***  
20180824  
增加 calypso.py 用来将物种丰度表的结果文件处理成 calypso 软件可以上传的格式；  

***
20180920  
好久没更新，因为没怎么写代码  
重新写了 PCA 的 R 代码，增加两个主坐标的差异检验，并且标注显著差异的值，将三张图输出在一个 PDF;  
同时会更新 PCoA.R 的代码;  
部分参考链接:  
[R语言可视化学习笔记之添加p-value和显著性标记 | Logos](https://ytlogos.github.io/2017/06/25/R%E8%AF%AD%E8%A8%80%E5%8F%AF%E8%A7%86%E5%8C%96%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8B%E6%B7%BB%E5%8A%A0p-value%E5%92%8C%E6%98%BE%E8%91%97%E6%80%A7%E6%A0%87%E8%AE%B0/)  
[R语言grid包使用笔记——viewport](https://blog.csdn.net/vivihe0/article/details/47188329)  
[将多张图输出到一个或者多个 PDF 上](http://www.sthda.com/english/articles/24-ggpubr-publication-ready-plots/81-ggplot2-easy-way-to-mix-multiple-graphs-on-the-same-page/)  

***
20180924  
乘着中秋放假，增加 adonis 分析的脚本 adonis.R, 比较简单，后边肯定还得继续完善;  
祝自己中秋快乐咯，需要努力学习;  
只剩下钢琴陪我谈了一天;  
参考链接: [RPubs - Multivariate analyses of variance](https://rpubs.com/collnell/manova)  

***
20180926  
增加了帮 Neko 写的一个脚本 run_Combine_gvcf.py，她要走啦，留作纪念好了  

***
20181008  
修改了 PCA 和 PCoA 的脚本，之前没有考虑到差异结果没有显著的情况，导致报错；  
果然不断的迭代才是好的方法，你不可能一次性把所有情况考虑清楚的。不过第一次还是尽可能的多考虑；  

***  
20181022  
越来越忙了，增加了批量生成 metawrap 组装的脚本 getScript.py，果然需要批量生成..任何手动的东西真是太可恶了！  

***  
20181023  
增加了 anova 的脚本 anova.R，包括方差齐性检验，正态分布检验，mean+se 的柱状图输出。断断续续终于写完了，还不是很完善，也没有弄成通用的，因为时间
不怎么够用，等下下次需要用的时候再改吧。 写得过程中参考了很多有用的博客，如 [One-Way ANOVA Test in R - Easy Guides - Wiki - STHDA](http://www.sthda.com/english/wiki/one-way-anova-test-in-r), [Plotting means and error bars (ggplot2)](http://www.cookbook-r.com/Graphs/Plotting_means_and_error_bars_(ggplot2)/), 非常感谢~ 同时好多想要的功能也没有完善，后续有需要再修改吧。  

***  
20181024  
增加了一个 python 脚本，SelectandMerge.py， 项目分析中用到；  

***  
20190420  
久违的更新，距离上一次已经 6 个月了... 自己仍旧没有取得特别大的进步，这次是增加了多元线性回归的一个脚本 multiple_liner.R，勉强把这个东西大致弄懂了，待完善，要去吃晚饭..  

***  
20200311  
将近一年了... 没有写这个文档，回头看还是蛮有感触的... 这大概是记录的意义所在吧~  
增加了 paper_information.py 脚本，用于输入文献官网网址，爬取杂志名称，发表时间，影响因子等信息，待完善补充；  

***  
2020年3月11日 下午9:38  
良心发现，加快更新（其实是因为在整理项目）； 增加了表型处理的脚本 abnormal_values.py ，包括缺失值和异常值，待完善；  


***  
2020年3月13日 上午8:50  
增加了三组差异检验箱线图的显著性标识生成脚本 diff_label.py, 待完善；芒格说，每天进步一点点，加油~  

   
***  
2020年3月15日 上午11:08  
增加了三个脚本，分别是离散型变量表型的差异检验：cat_diff.R， 以及其结果整理的脚本：cat_result.py， 还有连续型表型变量的差异检验的结果整理：con_result.py， 待完善； 我说：即使状态再差，也有自己能做的事情；  

***  
2020年3月15日 下午9:19  
增加了倾向性评分脚本 propensity_score.R 待完善; 相应的博客文章见这里[倾向性评分 | Propensity score](https://nonewood.github.io/2020/03/15/propensity-score/)  
是一个充实的周末没错了... 略累... 待会儿去画画；  

#直接画患者和健康人的差异物种, 门水平
library(ggplot2)
library(dplyr)
dt = read.table('phylum_boxplot.txt', header=T)

group_list = "NCA:sCAD:AMI"
color_list = "24af2d:ea5e74:e80211"
#tax_list = "Firmicutes:Bacteroidetes:Proteobacteria:Actinobacteria:Verrucomicrobia:Euryarchaeota:Viruses_noname:Fusobacteria:Synergistetes:Candidatus_Saccharibacteria"
tax_list = "Verrucomicrobia:Synergistetes"
legend_list = c(unlist(strsplit(group_list, ":")))
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
tax_order = c(unlist(strsplit(tax_list, ":")))

dt$group_order<-factor(dt$Group, legend_list)
dt$ID_order<-factor(dt$ID, tax_order)
p = ggplot(dt,aes(x = ID_order, y = log10(Abd))) +
geom_boxplot(aes(fill = factor(group_order)), fatten = 1, lwd = 0.5, outlier.size = 0.5, position = position_dodge(0.8)) +
labs(x ='', y = "Relative~abundance", fill = '', color = '', size = 10 ) +
scale_fill_manual(values = color_var) + 
theme(
    axis.text = element_text(colour = 'black', size = 10),
    axis.text.x = element_text(angle = 0),
    #axis.text.x = element_text(hjust = 1, angle = 0), #phylum
#   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #genus
#   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 60), #species
    axis.title.y = element_text(size = 10, face = 'bold'),
    axis.line = element_line(size=0.5, colour = "black"),
    #legend.position = c(0,0),
    legend.justification = c(0,0),
    legend.key = element_blank(),
    legend.text = element_text(size = 8),
    legend.key.width = unit(0.15, 'in'),
    legend.key.height = unit(0.15, 'in'),
    legend.background = element_blank(),
    panel.background = element_blank(),
    plot.margin = unit(c(0.2, 0.2, 0.1, 0.2), 'in')
)
postscript(paste("phylum_boxplot.eps",sep=""), width = 6, height=4)
pdf(paste("phylum_boxplot.pdf",sep=""), width = 6, height=4)
p
dev.off()


## 种水平
library(ggplot2)
library(dplyr)
dt = read.table('species_boxplot.txt', header=T)

group_list = "NCA:sCAD:AMI"
color_list = "24af2d:ea5e74:e80211"
tax_list = "Alistipes_onderdonkii:Coprococcus_sp_ART55_1:Megasphaera_unclassified:Dialister_succinatiphilus:Lactobacillus_amylovorus:Lactobacillus_salivarius:Lactobacillus_mucosae:Lactobacillus_crispatus:Enterobacter_cloacae:Coprococcus_eutactus:Phascolarctobacterium_succinatutens:Bifidobacterium_bifidum:Citrobacter_unclassified:Citrobacter_freundii:Prevotella_stercorea:Sutterella_wadsworthensis:Prevotella_bivia:Fusobacterium_mortiferum:Prevotella_disiens:Elizabethkingia_unclassified"
legend_list = c(unlist(strsplit(group_list, ":")))
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
tax_order = c(unlist(strsplit(tax_list, ":")))

dt$group_order<-factor(dt$Group, legend_list)
dt$ID_order<-factor(dt$ID, tax_order)
p = ggplot(dt,aes(x = ID_order, y = log10(Abd))) +
    geom_boxplot(aes(fill = factor(group_order)), fatten = 1, lwd = 0.5, outlier.size = 0.5, width = 0.8, position = position_dodge(0.8)) +
   # labs(x ='', y = expression(Relative~abundance~(log['10'])), fill = '', color = '', size = 10 ) +
    labs(x ='', y = "Relative abundance", fill = '', color = '', size = 10 ) +
    geom_vline(xintercept=c(14.5), linetype="dotted") + 
    scale_fill_manual(values = color_var) +
    theme(
        axis.text = element_text(colour = 'black', size = 10),
        #    axis.text.x = element_text(angle = 0),
        #axis.text.x = element_text(hjust = 1, angle = 0), #phylum
        #   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #genus
        axis.text.x = element_text(hjust = 1, face = 'italic', angle = 60), #species
        axis.title.y = element_text(size = 10, face = 'bold'),
        axis.line = element_line(size=0.5, colour = "black"),
        #legend.position = c(0,0),
        legend.justification = c(0,0),
        legend.key = element_blank(),
        legend.text = element_text(size = 10),
        legend.key.width = unit(0.2, 'in'),
        legend.key.height = unit(0.2, 'in'),
        legend.background = element_blank(),
        panel.background = element_blank(),
        plot.margin = unit(c(0.2, 0.2, 0.1, 0.2), 'in')
    )
#postscript(paste("species_boxplot.eps",sep=""), width = 8, height=5)
pdf(paste("species_boxplot.pdf",sep=""), width = 8, height=4)
p
dev.off()

## 五个种水平
library(ggplot2)
library(dplyr)
dt = read.table('five_species_boxplot.txt', header=T)

group_list = "NCA:sCAD:AMI"
color_list = "24af2d:ea5e74:e80211"
#tax_list = "Alistipes_onderdonkii:Coprococcus_sp_ART55_1:Megasphaera_unclassified:Dialister_succinatiphilus:Lactobacillus_amylovorus:Lactobacillus_salivarius:Lactobacillus_mucosae:Lactobacillus_crispatus:Enterobacter_cloacae:Coprococcus_eutactus:Phascolarctobacterium_succinatutens:Bifidobacterium_bifidum:Citrobacter_unclassified:Citrobacter_freundii:Prevotella_stercorea:Sutterella_wadsworthensis:Prevotella_bivia:Fusobacterium_mortiferum:Prevotella_disiens:Elizabethkingia_unclassified"
tax_list = "Alistipes_onderdonkii:Lactobacillus_mucosae:Lactobacillus_crispatus:Pyramidobacter_piscolens:Atopobium_parvulum"
legend_list = c(unlist(strsplit(group_list, ":")))
color_var = unlist(strsplit(color_list, ":"))
color_var = c(paste("#",color_var,sep=""))
tax_order = c(unlist(strsplit(tax_list, ":")))

dt$group_order<-factor(dt$Group, legend_list)
dt$ID_order<-factor(dt$ID, tax_order)
p = ggplot(dt,aes(x = ID_order, y = log10(Abd))) +
    geom_boxplot(aes(fill = factor(group_order)), fatten = 1, lwd = 0.5, outlier.size = 0.5, width = 0.8, position = position_dodge(0.8)) +
   # labs(x ='', y = expression(Relative~abundance~(log['10'])), fill = '', color = '', size = 10 ) +
    labs(x ='', y = "Relative abundance", fill = '', color = '', size = 10 ) +
    #geom_vline(xintercept=c(14.5), linetype="dotted") + 
    scale_fill_manual(values = color_var) +
    theme(
        axis.text = element_text(colour = 'black', size = 10),
        #    axis.text.x = element_text(angle = 0),
        #axis.text.x = element_text(hjust = 1, angle = 0), #phylum
        #   axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #genus
        axis.text.x = element_text(hjust = 1, face = 'italic', angle = 45), #species
        axis.title.y = element_text(size = 10, face = 'bold'),
        axis.line = element_line(size=0.5, colour = "black"),
        #legend.position = c(0,0),
        legend.justification = c(0,0),
        legend.key = element_blank(),
        legend.text = element_text(size = 10),
        legend.key.width = unit(0.2, 'in'),
        legend.key.height = unit(0.2, 'in'),
        legend.background = element_blank(),
        panel.background = element_blank(),
        plot.margin = unit(c(0.2, 0.2, 0.1, 0.2), 'in')
    )
#postscript(paste("species_boxplot.eps",sep=""), width = 8, height=5)
pdf(paste("five_species_boxplot.pdf",sep=""), width = 8, height=4)
p
dev.off()

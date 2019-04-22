#!/usr/bin/Rscript
############################################################
# 脚本越来越多....哭泣..
############################################################

library(ggplot2)
library(grid)
library(dplyr)
library(getopt)
args <- commandArgs(trailingOnly = FALSE)
program <- sub("--file=", "", args[grep("--file=", args)])

#SCRIPTPATH <- dirname(program)
#source(paste(SCRIPTPATH,'/ggplot2_themes.R',sep=''))
#source('./ggplot2_themes.R')

spec <- matrix(c(
    'help','h',0,'logical','',
    'barplot.txt','i',1,'character','input YL OTU per table',
    'legendID','t',1,'character','the legend ID in order (tax or otu), separated by colon',
    'sampleOrder','s',1,'character','the sample ID in order, separated by colon',
    'group_name','r',1,'character','the group names in order, separated by colon',
    'colorID','c',2,'character', 'the color set for plot, separated by colon',
    'prefix','p',1,'character', 'the prefix for output file',
    'outdir','o',2,'character','output dir',
    'log','l',2,'character','log file'
),ncol=5,byrow=TRUE)
opt <- getopt(spec)
#cat(getopt(spec, usage=TRUE))

# if help was asked for print a friendly message
# and exit with a non-zero error code
if( !is.null(opt$help)) {
        cat(getopt(spec, usage=TRUE));
        q(status=1);
}

if( is.null(opt$outdir) ) { opt$outdir <- './'}
if( is.null(opt$frequency)) {opt$frequency <- 0.8}
if( is.null(opt$log)) {opt$log <- 'log.txt'}

Sys.setenv(TZ="Asia/Shanghai")
#Sys.getenv("TZ")
cat("group_barplot.R program starts at:", format(Sys.time(), "%a %b %d %X %Y"),'\n',append=TRUE,file=opt$log)
##########
## process input parameters
dt <- read.table(opt$barplot.txt, header=T, sep="\t")
legendID <- unlist(strsplit(opt$legendID, ":"))
sampleOrder <- unlist(strsplit(opt$sampleOrder, ":"))
group_name <- unlist(strsplit(opt$group_name, ":"))
if( !is.null(opt$colorID) ) { colorID <- c(paste("#",unlist(strsplit(opt$colorID, ":")),sep=""))}
# 以后完善同一组内排序的问题吧..
#if( !is.null(opt$x_order)) {
#	x_order <- c(paste("#",unlist(strsplit(opt$x_order, ":")),sep=""))
#	dt$individual_order = factor(dt$individual, level=x_order)
#}
dt$order <- factor(dt$SamplingTime, levels=group_name)
dt$SampleID <- factor(dt$SampleID, levels=sampleOrder)
outfile = paste(opt$prefix,'barplot.pdf', sep='_')
pdf(paste(opt$outdir,outfile,sep="/"), width = 8, height = 6, onefile=FALSE)

p = ggplot(dt,aes(x=dt$SampleID,y=dt$Abundance, fill=factor(dt$Tax, levels= rev(legendID)))) +
    geom_bar(stat = "identity", color = "#56666B", size = 0.1) +
	scale_fill_manual(values= rev(colorID)) +
    labs(x = "", y = "Relative Abundance") +
    theme_bw() +
    theme(axis.title = element_text(size = 10),
          axis.text = element_blank(),
		  axis.ticks = element_blank(),
#          axis.text = element_text(colour = "black", size = 10),
#          axis.text.x = element_text(hjust = 1,angle=65,color="black"),
          legend.title = element_blank(),legend.key.size=unit(3,"mm"),
          legend.text=element_text(size=10)) +
          facet_wrap(~order, strip.position = "bottom", nrow = 1, scales="free_x")
gt = ggplotGrob(p)
N<- dt%>% group_by(order)%>% summarise(count = length(unique(SampleID)))
panelI <- gt$layout$l[grepl("panel", gt$layout$name)]
gt$widths[panelI] <- unit(N$count, "null")
grid.newpage()
grid.draw(gt)
dev.off()

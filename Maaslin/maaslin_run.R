library(getopt)
spec <- matrix(c(
    'help','h',0,'logical','',
    'input','i',1,'character','the tsv file',
    'config','c',1,'character','the config file',
    'outdir','o',2,'character','output dir'
),ncol=5,byrow=TRUE)
opt <- getopt(spec)
if( !is.null(opt$help)) {
        cat(getopt(spec, usage=TRUE));
        q(status=1);
}

if ( is.null(opt$input) | is.null(opt$config)) {
	print('Please!')  #翻译过来是求您了！
	cat(getopt(spec, usage=TRUE));
	q(status=1);
}

input = opt$input
config = opt$config
if( is.null(opt$outdir) ) { outdir <- './'} else { outdir <- opt$outdir }
library(Maaslin)
Maaslin(input, outdir, strInputConfig=config ,dMinAbd=0,dMinSamp = 0)

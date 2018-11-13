#! /usr/bin/python3
import argparse,os,shutil,re,glob
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Convert the kark file of kraken2 to some new for krona sofaware.
Example: python3 kraken_trans.py -i krakfile -o outdir
To be continued.
------------------'''
)
parser.add_argument('-i','--Indir', help = "the directory of krakfile by kraken2.")
parser.add_argument('-o','--outdir',help = "the output directory, full path.")
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args = parser.parse_args()
(krakdir,outdir) = (args.Indir, args.outdir)
par = [krakdir,outdir]

if not all(par):
	parser.print_help()
	exit()

if os.path.exists(outdir):
	shutil.rmtree(outdir)

os.makedirs(outdir)
Taxid2Tax = dict()
with open('/ifswh1/BC_PS/wangpeng7/database/taxdump/taxonomy2sevenlevel.txt','r') as IN:
	for line in IN:
		line = line.strip('\n').split('\t')
		Taxid2Tax[line[0]] =  line[1]

for krakfile in glob.glob(krakdir + '/*krak'):
	basename = os.path.basename(krakfile)
	match = re.search('(.*).krak', basename)
	prefix = match.group(1)
	outfile = outdir + '/' + prefix + '.trans.krak'
	with open(krakfile,'r') as IN, open(outfile,'w') as out:
		for line in IN:
			lst = line.strip('\n').split('\t')
			seqId = lst[1]
			tax = lst[2]
			tax_match = re.search('taxid (\d+)', tax)
			taxId = tax_match.group(1)
			if taxId == '0':
				print (seqId + '\t' + 'Unclassified;Unclassified;Unclassified;Unclassified;Unclassified;Unclassified;Unclassified', file=out)
			elif taxId in Taxid2Tax:
				print(seqId + '\t' + Taxid2Tax[taxId], file=out)
	#		else:
	#			print(taxId + ' is not found! please check~')


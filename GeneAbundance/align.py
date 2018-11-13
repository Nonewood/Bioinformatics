#! /usr/bin/python3
import argparse,re,os,glob
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Generate the process directory and shell directory of soap alignment.
To be continued.
------------------'''
)
parser.add_argument('rmhost', help = "the removehost fastq file list.")
parser.add_argument('soap', help = "soap path.")
parser.add_argument('index', help = "the index file directory.")
parser.add_argument('outdir',help = "the output directory,default is current working directory.",nargs='?')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args=parser.parse_args()
(listfile,soap_path,index_dir) = (args.rmhost, args.soap, args.index)
par = [listfile,soap_path,index_dir]
outdir = args.outdir if args.outdir else './'

if not os.path.exists(outdir):
	os.makedirs(outdir)	

index_list = list()
for item in glob.glob(index_dir + '/all_assembly.fasta.index.amb'):
#for item in glob.glob(index_dir + '/AA11A_final_assembly.fasta.index.amb'):
#for item in glob.glob(index_dir + '/AA12A_final_assembly.fasta.index.amb'):
#for item in glob.glob(index_dir + '/AA4A_final_assembly.fasta.index.amb'):
	match = re.search('(.*)\.amb', item)
	index = match.group(1)
	index_list.append(index)
index_par = '-D ' + ' -D '.join(index_list)
#print(index_par)

with open(listfile,'r') as IN:
	for line in IN:
		lst = line.strip('\n').split('\t')
		(sampleID,fq1,fq2) = (lst[0],lst[1],lst[2])
		processPath = outdir + '/Process/' + sampleID
		shellPath = outdir + '/Shell/' + sampleID
		if not os.path.exists(processPath):
			os.makedirs(processPath)
		if not os.path.exists(shellPath):
			os.makedirs(shellPath)		
		filepath = shellPath + '/' + sampleID + '.sh'
		outpe = processPath + '/' + sampleID + '.soap.pe'
		outse = processPath + '/' + sampleID +'.soap.se'
		outlog = processPath + '/' + sampleID +'.soap.log'	
		para = '-m 200 -x 1000 -r 2 -v 13 -p 12 -l 32 -s 75 -c 0.95'
		shell = ' '.join([soap_path,'-a',fq1,'-b',fq2, index_par,'-o',outpe,'-2',outse,para])
		with open (filepath,'w') as out:
			out.write(shell + ' 2>' + outlog + '\n')
			out.write('gzip -f ' + outpe + '\n')
			out.write('gzip -f ' + outse + '\n')

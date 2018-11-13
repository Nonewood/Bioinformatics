#! /usr/bin/python3
import pandas as pd
import argparse,os,shutil,re
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Generate the profile files(kingdom, phylum, genus..) for all samples of kraken2 results.
Example: python3 kraken.py -i /ifswh1/BC_COM_P2/F18FTSNCWLJ0169/HUMnzsM/HUMrfvM/metawrap/Kraken/sampleID -d /ifswh1/BC_COM_P2/F18FTSNCWLJ0169/HUMnzsM/HUMrfvM/metawrap/Kraken/KRAKEN -l kingdom,phylum,class,order,family,genus,species -o /ifswh1/BC_COM_P2/F18FTSNCWLJ0169/HUMnzsM/HUMrfvM/metawrap/Kraken/KRAKEN/Outdir
To be continued.
------------------'''
)
parser.add_argument('-i','--sampleID', help = "the sample id list file, tab separated.")
parser.add_argument('-d','--directory', help = "the kraken2 output directory.")
parser.add_argument('-l','--level', help = "choose the taxonomic levels for profile files, semicolon(,) separated. (optional:kingdom,phylum,class,order,family,genus,species), default is phylum,genus,species.", nargs='?')
parser.add_argument('-o','--outdir',help = "the output directory, full path.")
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args = parser.parse_args()
(IDlist, directory, outdir) = (args.sampleID, args.directory, args.outdir)
par = [IDlist, directory, outdir]

if not all(par):
	parser.print_help()
	exit()

levels = args.level if args.level else 'phylum,genus,species'
level_list = levels.split(',')

if os.path.exists(outdir):
	shutil.rmtree(outdir)
	
os.makedirs(outdir)
with open(IDlist, 'r') as idfile:
	for line in idfile:
		idlist= line.strip('\n').split('\t')		
		for sample in idlist:
			krakfile = directory + '/' + sample + '.RemoveHost.krak'
			reportfile = directory + '/' + sample + '.RemoveHost.report'
			line_number = os.popen('wc -l ' + krakfile).read()
			reads_number = line_number.split(' ')[0]			
			with open(reportfile, 'r') as report:
				for line in report:
					line = line.strip('\n')
					lst = line.split('\t')
					name_list = lst[0].split('|')
					if 'kingdom' in level_list:
						filename =  outdir + '/' + sample + '_kingdom_profile.temp'
						if re.match('d__',name_list[-1]):
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Kingdom:
								print(name_list[-1] + '\t' + str(rate), file=Kingdom)
		# Phylum	
					if 'phylum' in level_list:
						filename = outdir + '/' + sample + '_phylum_profile.temp'
						if re.match('p__',name_list[-1]): 
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Phylum:
								print(name_list[-1] + '\t' + str(rate), file=Phylum)
		# Class	
					if 'class' in level_list:
						filename = outdir + '/' + sample + '_class_profile.temp'
						if re.match('c__',name_list[-1]): 
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Class:
								print(name_list[-1] + '\t' + str(rate), file=Class)
		# Order
					if 'order' in level_list:
						filename = outdir + '/' + sample + '_order_profile.temp'		
						if re.match('o__',name_list[-1]): 
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Order:
								print(name_list[-1] + '\t' + str(rate), file=Order)
		#Family
					if 'family' in level_list:
						filename = outdir + '/' + sample + '_family_profile.temp'
						if re.match('f__',name_list[-1]): 
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Family:
								print(name_list[-1] + '\t' + str(rate), file=Family)
					
		#Genus
					if 'genus' in level_list:
						filename = outdir + '/' + sample + '_genus_profile.temp'
						if re.match('g__',name_list[-1]): 
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Genus:
								print(name_list[-1] + '\t' + str(rate), file=Genus)

		#Species 
					if 'species' in level_list:
						filename = outdir + '/' + sample + '_species_profile.temp'
						if re.match('s__',name_list[-1]): 
							rate = int(lst[1])/int(reads_number)
							with open(filename, 'a') as Species:
								print(name_list[-1] + '\t' + str(rate), file=Species)	

# merge and output
for tax in level_list:
	frame = pd.DataFrame()
	dt_list = list()
	with open(IDlist, 'r') as idfile:
		for line in idfile:
			idlist= line.strip('\n').split('\t')
			for sample in idlist:
				filename = outdir + '/' + sample + '_' + tax + '_profile.temp'
				df = pd.read_table(filename,names=[sample], index_col = 0)
				dt_list.append(df)
			frame = pd.concat(dt_list, axis=1)
			frame.fillna(value=0, inplace=True)
			outname =  outdir + '/' + tax + 'ProfileTable.xls'
			frame.to_csv(outname,sep='\t') 

needremove = outdir + '/*profile.temp'
os.system('rm ' + needremove)

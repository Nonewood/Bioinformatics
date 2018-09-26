#! /usr/bin/python3
import argparse,re,os,math,glob
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Combine the gvcf files into vcf file.
Example: python3 run_Combine_gvcf.py -i allSample.list -t intervals.list -r gvcfDir.list -o Test -q qsub.sh
To be continued.
------------------'''
)
parser.add_argument('-i','--Input', help = "the sampleID file.")
parser.add_argument('-t','--Interval', help = "the intervals list file.")
parser.add_argument('-r','--gvcf', help = "the gvcf file directory list file.")
parser.add_argument('-o','--outdir', help = "the outdir.")
parser.add_argument('-q','--qsub', help = "the final qsub file.")
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args = parser.parse_args()
sampleList = args.Input
intervalsList = args.Interval
gvcfDir = args.gvcf
outdir = args.outdir
qsub = args.qsub
par = [sampleList,intervalsList,gvcfDir,outdir,qsub]

if not all(par):
    parser.print_help()
    exit()

if os.path.isfile(qsub):
    os.remove(qsub)

SampleDir = dict()
with open(gvcfDir,'r') as IN:
    for line in IN:
        gvcf_dir = line.strip('\n')
        for item in glob.glob(gvcf_dir + '/*'):
            key = item.split('/')[-1]
            SampleDir[key] = gvcf_dir

with open(intervalsList,'r') as IN:
    for line in IN:
        interLine = line.strip('\n')
        Chr = interLine.split('/')[-2]
        chrdir = '/'.join([outdir,Chr])

        if not os.path.isdir(chrdir):
            os.makedirs(chrdir)

        gvcfs = ''
        with open(sampleList,'r') as Sample:
            for sampleline in Sample:
                sampleID = sampleline.strip('\n')
                gatkName = '.'.join([sampleID,Chr,'g.vcf.gz'])
                if sampleID in SampleDir:
                    eachGvcf = '/'.join([SampleDir[sampleID],sampleID,'callGVCF_GATK',gatkName])
                else:
                    print('Error: sample ID: ' + sampleID + ' is not in the gvcf dir,please check your file.')
                gvcfs = gvcfs + " --variant " + eachGvcf
        prefix = os.path.basename(interLine).replace(".intervals", "")
        outgvcf = chrdir + "/" + prefix + ".g.vcf.gz"
        shell = chrdir + "/CombineGvcf_" + prefix + ".sh"
        with open(shell,'w') as out:
            out.write('set -e\necho Start at : `date`\n')
            shell_line = " ".join(["java -Xmx10g -Djava.io.tmpdir=" + outdir, "-jar /zfssz2/BC_COM_P7/F17HTSCCWLJ1810/HUMqqmR/s8.gvcf/bin/GenomeAnalysisTK.jar -R /zfssz2/BC_COM_P7/F17HTSCCWLJ1810/HUMqqmR/s8.gvcf/hg19_fa/hg19.fasta -T CombineGVCFs", gvcfs, "-o", outgvcf, "-L", interLine]) + "\n"
            out.write(shell_line)
            out.write("echo End at : `date`\n")
            out.write("echo Work is completed! > " + shell + ".sign\n")
        with open (qsub,'a') as out:
            out.write("qsub -o %s -e %s -l vf=2G,p=1 -q bc.q -P HUMrqkR %s\n" % (chrdir, chrdir, shell))

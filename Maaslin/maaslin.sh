#! /bin/bash
Rscript tsvGeneration.R diff_NCA_AMI_speciesProfileTable.xls phenotype.update.xls Group:Gender:Age NCA:AMI NCA_AMI ./
python3 config_generate.py NCA_AMI_Group_Gender_Age.tsv 4
Rscript maaslin_run.R -i NCA_AMI_Group_Gender_Age.tsv -c generated_config -o outdir

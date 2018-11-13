for file in /ifswh1/BC_COM_P2/F18FTSNCWLJ0169/HUMnzsM/HUMrfvM/metawrap/GeneAbundance/Outdir/Shell/*
do 
	if test -d $file
	then
		cd $file 
		for script in ${file}/*sh
		do
			qsub -cwd -l vf=5G,p=1 -P HUMrfvM -q bc.q $script
		done
	fi
done

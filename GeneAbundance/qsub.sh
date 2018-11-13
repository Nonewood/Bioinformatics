for file in shell_dir/*
do 
	if test -d $file
	then
		cd $file 
		for script in ${file}/*sh
		do
			qsub -cwd -l vf=XG,p=1 -P XXX -q xx.q $script
		done
	fi
done

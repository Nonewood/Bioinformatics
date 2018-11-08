# 和 dta_delivery_scp.expect 联用，实现批量传输
#! /bin/bash
list_file=$1   #file path each line
dest_dir=$2 #the destination directory
cat $list_file | while read line
do
echo "Processing file:scp the $line to $dest_dir"
expect data_delivery_scp.expect $line $dest_dir
done

#! /bin/bash
#exampel sh data_delivery_rsyncs.sh file.list Temp  account  password IP
list_file=$1   #file_path or dir_path (permit the soft link  each line
dest_dir=$2 #the destination directory
account=$3 #your account
password=$4 #your password
ip=$5 #destination IP
cat $list_file | while read line
do
echo "Processing file:rsync the $line to $dest_dir"
expect data_delivery_rsync.expect $line $dest_dir $account $password $ip
done

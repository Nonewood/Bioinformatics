# 传输文件到 Mac 端
for x in `ls */*pdf`
do
	expect scp.expect $x beta
done

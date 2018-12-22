# 发现 mac 下没有找到合适的 md5 校验工具，所以写了个脚本，用于和 linux 下 md5sum 产生的文件 md5 值进行校验，较简略
import re,os
os.system('md5 *gz > temp.md5')
# transform 转化格式
with open('temp.md5','r') as IN, open('new.md5', 'w') as out:
    for line in IN:
        match = re.search('MD5 \((.*)\) = (\w+)',line)
        if match:
            print(match.group(2) + '  ' + match.group(1), file=out)

#比较前后文件的 md5
Dcit = dict()
with open('md5.txt','r') as IN:
    for line in IN:
        lst = line.strip('\n').split('  ')
        Dcit[lst[0]] = lst[1]
with open('new.md5','r') as IN:
    for line in IN:
        lst = line.strip('\n').split('  ')
        if lst[0] in Dcit:
            if Dcit[lst[0]] == lst[1]:
                continue
    #              print(lst[1] + ' is ok\n')
            else:
                print(lst[0] + ' is not ok!')

## 爬东财深股通，很粗糙的版本...
import requests,re
from bs4 import BeautifulSoup
url = 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid=f62&fs=b:BK0804&stat=1&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124&rt=53091671&cb=jQuery183020346281626049056_1592750139884&_=1592750150231'
res = requests.get(url)
soup = BeautifulSoup(res.content, "html.parser")
content = soup.get_text().split('},{')
# f12, f14, f62 , f66, f72 , f78 ,f84
print('\t'.join(['代码','名称', '主力净流入', '超大单净流入', '大单净流入', '中单净流入', '小单净流入']))
for x in content:
    match = re.search('\"f12\":\"(.*?)\".*\"f14\":\"(.*?)\".*\"f62\":(.*?),.*\"f66\":(.*?),.*\"f72\":(.*?),.*\"f78\":(.*?),.*\"f84\":(.*?),', x)
    (code, name, main, sup, big, mid, sml) = (match.group(1), match.group(2),match.group(3), match.group(4), match.group(5), match.group(6), match.group(7) )
    print('\t'.join([code, name, main, sup, big, mid, sml])) 

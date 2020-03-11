#输入文献网址，获取文献题目，杂志名称，影响因子，发表日期
#V1 目前只适合 Nature + cell 系列杂志，其他待测试，因为每个杂志的网站代码写法不一样；
#昨晚看了关注的博主的一段话，我觉得很有道理，自己还是太懒了，而且也太笨了；
#人生苦短，一切遵守 KISS 原则。持续构建一套自己都觉得很爽的灵活够用的渗透测试方法论，需要借用的借用，需要脚本化的脚本化，需要 Web 化的 Web 化，需要工程化的工程化，需要产品化的产品化，需要赚钱的赚钱，需要开源的开源。这里有一个关键点：团队作战，共同进步:-)
#共勉

#nature 系列
import requests,re
from bs4 import BeautifulSoup
url = 'https://www.nature.com/articles/s41467-020-14676-4'
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")
content = soup.prettify()
soup_match = re.search('datetime="(.*?)"', content) ## 非贪婪匹配
date = soup_match.group(1)
name = soup.find(class_ = 'c-article-info-details').get_text().split('\n')[1]
title = soup.find(class_ = 'c-article-title u-h1').get_text().split('\n')[0]

import pandas as pd
dt = pd.read_table('IF_2019.txt', index_col = 1) # 这个文件每年更新，在当前目录下
IF_dict = dt['Journal Impact Factor'].to_dict()
for x in IF_dict:
    match = re.search(name, x, flags=re.IGNORECASE)
    if match:
        IF = IF_dict[x]
        
print(title)        
print(name + ' | IF:' + IF  + ' | Date ' + date )


# cell 系列
import requests,re
from bs4 import BeautifulSoup
url = 'https://www.cell.com/cell/fulltext/S0092-8674(20)30160-4?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0092867420301604%3Fshowall%3Dtrue'
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")

date = soup.find(class_ = 'article-header__publish-date__value').get_text().split('\n')[0]
name_pre = soup.find(class_ = 'upsell-box__banner upsell-box__control').get_text().split('\n')[0]
name = re.sub('Subscribe to ','', name_pre)
title = soup.find(class_ = 'article-header__title').get_text().split('\n')[0]

import pandas as pd
dt = pd.read_table('/Users/tongxueer/Documents/文献/IF_2019.txt', index_col = 1)
IF_dict = dt['Journal Impact Factor'].to_dict()
for x in IF_dict:
    match = re.search(name, x, flags=re.IGNORECASE)
    if match:
        IF = IF_dict[x]
print(title)  
print(name + ' | IF:' + IF  + ' | Date ' + date )

# Bioinformatic 这个杂志爬取失败....


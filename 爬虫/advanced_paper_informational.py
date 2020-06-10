from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys  #这个没有用上
import time,os,re

# browser = webdriver.Chrome()  # 这个是模拟浏览器打开.. 
op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(options=op) #op 这三行可以不用打开浏览器..
url = 'https://pubmed.ncbi.nlm.nih.gov/'


out = open('paper_information.xls', 'w')
doi_list = ['DOI: 10.1016/S0140-6736(19)32319-0', 'DOI: 10.1038/s41575-019-0209-8','DOI: 10.1016/j.tips.2019.04.006','DOI: 10.1038/nrc2857', 'DOI: 10.1038/ismej.2015.11', 'DOI: 10.1038/s41591-018-0160-1']          
        
# 杂志名称全称
j_name = dict()
with open('J_Medline.txt', 'r') as IN:
    for line in IN:
        line = line.strip('\n')
        if line.startswith('JournalTitle'): 
            if re.search(' \(.*\)', line): #发现有带（London, England）这种信息的。。。。
                match = re.search('JournalTitle: (.*) \(.*\)', line) 
            else:
                match = re.search('JournalTitle: (.*)', line) # ncbi 是缩写，然后影响因子是全称，所以得找到这个信息
            full = match.group(1)
        if line.startswith('MedAbbr'):
            match = re.search('MedAbbr: (.*)', line)
            abbr = match.group(1)
        if line.startswith('NlmId'):
            j_name[abbr] = full
            
# 杂志 IF
import pandas as pd
dt = pd.read_table('IF_2019.txt', index_col = 1)
IF_dict = dt['Journal Impact Factor'].to_dict()

for x in doi_list:
    DOI = x
    browser.get(url)
    time.sleep(3)
    browser.find_element_by_xpath('//*[@name="term"]').send_keys(x)
    time.sleep(2)
    browser.find_element_by_xpath('//*[@class="search-btn"]').click()
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    # journal name abbr
    journal = soup.find(id = "full-view-journal-trigger").get_text().strip()

    # title
    title = soup.find(class_ = "heading-title").get_text().strip()
        
    # IF
    for x in IF_dict:
        match = re.search('^' + j_name[journal] + '$', x, flags=re.IGNORECASE) # 有的名字包含其他杂志的全称... 
        if match:
            IF = IF_dict[x]
            journal_name = j_name[journal]
        else:
            match = re.search('^' + j_name[journal].replace('.','') + '$', x, flags=re.IGNORECASE)  # 有的杂志匹配出来的全称多了个点：Nature reviews. Immunology
            if match:
                journal_name = j_name[journal].replace('.','')
                IF = IF_dict[x]


    # 发表时间
    if soup.find(class_ = "secondary-date"):
        p_time = soup.find(class_ = "secondary-date").get_text().strip().strip('Epub ').strip('.')
    else:
        p_time = soup.find(class_ = "cit").get_text().split(";")[0]

    # PMID 
    PMID = soup.find(class_ = "current-id").get_text()


    #原文链接
    doi_info = soup.find(class_ = "identifier doi") 
    http = doi_info.find(class_ = "id-link")['href'] # 增加这一步是因为偶尔会出现 NCBI 的链接

    # 一作和通讯
    authors = soup.find(class_ = "authors-list").get_text().strip().replace(u'\xa0', '').replace(u'\xa0', '').replace(' ', '')
    author_list = re.sub('\n\w*', '', authors).split(',')
    first_author = author_list[0]
    corresponding_author = author_list[-1]

    # 第一单位
    affiliations = soup.find(class_ = "affiliations").get_text().strip()
    affiliations = re.sub('[ ]+', ' ', affiliations)
    affiliations_list = re.sub('[\n]{2,}', '', affiliations).split('\n')
    first_affiliation = affiliations_list[1].lstrip(' 0123456789')

    line = '\t'.join([title, journal_name, p_time.replace('.', ''), PMID, DOI, http, IF, first_author, corresponding_author, first_affiliation])
    print(line, file = out)
    print(line)
    
out.close()

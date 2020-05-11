from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains   #这个也是
from selenium.webdriver.support.ui import Select # 这个也是
from selenium.webdriver.common.keys import Keys  #这个没有用上
import time,os,re
browser = webdriver.Chrome()
url = 'https://pubmed.ncbi.nlm.nih.gov/'
browser.get(url)
time.sleep(2)

out = open('paper_information.xls', 'w')

# 杂志名称全称
j_name = dict()
with open('/Users/PeZai/Downloads/J_Medline.txt', 'r') as IN:
    for line in IN:
        line = line.strip('\n')
        if line.startswith('JournalTitle'):
            match = re.search('JournalTitle: (.*)', line)
            full = match.group(1)
        if line.startswith('MedAbbr'):
            match = re.search('MedAbbr: (.*)', line)
            abbr = match.group(1)
        if line.startswith('NlmId'):
            j_name[abbr] = full
            
# 杂志 IF
import pandas as pd
dt = pd.read_table('/Users/Pezai/Documents/文献/IF_2019.txt', index_col = 1)
IF_dict = dt['Journal Impact Factor'].to_dict()

#下边这个是文献名字list
title_list = ['Gut microbiome and serum metabolome alterations in obesity and after weight-loss intervention', 'Distinct gut metagenomics and metaproteomics signatures in prediabetics and treatment-naïve type 2 diabetics']

for x in title_list:
    browser.find_element_by_xpath('//*[@name="term"]').clear() #清除搜索框的东西；
    browser.find_element_by_xpath('//*[@name="term"]').send_keys(x)
    browser.find_element_by_xpath('//*[@class="search-btn"]').click()
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    journal = soup.find(id = "full-view-journal-trigger").get_text().strip()

    # IF
    for x in IF_dict:
        match = re.search(j_name[journal], x, flags=re.IGNORECASE)
        if match:
            IF = IF_dict[x]


    # 发表时间
    p_time = soup.find(class_ = "secondary-date").get_text().strip().strip('Epub ').strip('.')

    # PMID 
    PMID = soup.find(class_ = "current-id").get_text()

    # DOI
    doi = soup.find(class_ = "id-link").get_text().strip()
    doi = 'DOI: ' + doi

    #原文链接
    doi_info = soup.find(class_ = "identifier doi") 
    http = doi_info.find(class_ = "id-link")['href'] # 增加这一步是因为偶尔会出现 NCBI 的链接，这样就只会爬取 doi 的官网链接了；

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

    line = '\t'.join([j_name[journal], p_time, PMID, doi, http, IF, first_author, corresponding_author, first_affiliation])
    print(line, file = out)
    print(line)
    
out.close()

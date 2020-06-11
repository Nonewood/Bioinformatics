from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys 
import time,os,re

# set pars
import argparse,re,os,math,glob
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Crawl the information of paper... You should provide the DOI or a file for DOI (line breaks). 
Example: python3 advanced_paper_informational.py -l 10.1016/S0140-6736(19)32319-0
         python3 advanced_paper_informational.py -f doi_file
To be continued.
------------------'''
)
parser.add_argument('-l','--onedoi', nargs='?', help = "DOI information.")
parser.add_argument('-f','--filelist',nargs='?', help = "the DOI information list file.")
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args = parser.parse_args()
var = args.onedoi
files = args.filelist 

## define the user（linux） and abbreviatio for print  
import re
Dict = {'zhangSan':'ZS', 'LiSi':'LS'}
import os
user_full = os.popen('whoami').readlines()[0].strip()
if user_full in Dict:
    user = Dict[user_full]
else:
    user = user_full

# doi information 
doi_list = list()
if var:
	doi_list.append('DOI: ' + var)
if files:
	with open(files, 'r') as IN:
		Input = IN.readlines()
		doi_list = ['DOI: ' + x.strip() for x in Input]	

# out file 
out = open('paper_information.xls', 'w')

## scraping 
print(user_full + ' is crawling... \nThe warning information appeared later does not matter. \nIt may need some time, please wait patiently:)\nIf there is no output for a long long time, you should stop it and try to run again.\n')

browser = webdriver.PhantomJS() 
url = 'https://pubmed.ncbi.nlm.nih.gov/'
        
# 杂志名称全称
j_name = dict()
with open('files/J_Medline.txt', 'r') as IN:
    for line in IN:
        line = line.strip('\n')
        if line.startswith('JournalTitle'):
            if re.search(' \(.*\)', line):
                match = re.search('JournalTitle: (.*) \(.*\)', line) 
            else:
                match = re.search('JournalTitle: (.*)', line) # ncbi 是缩写，然后影响因子是全称，所以得找到这个信息
            #发现有带（London, England）这种信息的。。。。
            full = match.group(1)
        if line.startswith('MedAbbr'):
            match = re.search('MedAbbr: (.*)', line)
            abbr = match.group(1)
        if line.startswith('NlmId'):
            j_name[abbr] = full
            
# 杂志 IF
import pandas as pd
dt = pd.read_table('files/IF_2019.txt', index_col = 1)
IF_dict = dt['Journal Impact Factor'].to_dict()

for x in doi_list:
    DOI = x
    browser.get(url)
    print("\nThe pubmed url is opening correctly.\n")
    time.sleep(3)
    try:
        browser.find_element_by_xpath('//*[@name="term"]').send_keys(x)
        time.sleep(2)
    except NoSuchElementException:
        print('AO, something wrong...')

    browser.find_element_by_xpath('//*[@class="search-btn"]').click()
    time.sleep(2)
    print("\nThe page for paper " + x  + " is opiening correctly.\n")
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

    line = '\t'.join([user, title, journal_name, p_time.replace('.', ''), PMID, DOI, http, IF, first_author, corresponding_author, first_affiliation])
    print(line, file = out)
    print('\n' + line + '\n')
    
out.close()
print("\nDone!, the output is paper_information.xls.\n")

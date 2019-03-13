#! /usr/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys  #这个没有用上
import time,os,re
browser = webdriver.Chrome()
url = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome'
browser.get(url)
otu_seq = 'filter_OTU_final.fasta' # 输入文件
seq = ''
#otu_num = 0
with open(otu_seq, 'r') as IN:
    for line in IN:
        seq = seq + line
#        otu_num += 1
browser.find_element_by_id("seq").send_keys(seq)
time.sleep(60)  # 视网速而定...
print("sequence input done~")
browser.find_element_by_xpath('//*[@class="blastbutton"]').click()
time.sleep(180) # 视网速而定...
print('blast done!')
out = open('align_result.xls', 'w')
select = Select(browser.find_element_by_id('queryList'))
number = len(select.options)
for index in range(0, number):
    select = Select(browser.find_element_by_id('queryList'))
    otu_id = select.options[index].text
    print(otu_id)
    print('##' + otu_id, file = out)
    select.select_by_index(index)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table = soup.find(class_ = "ui-ncbigrid-outer-div caption-exists")
    raw_head = table.find(class_ = "first").get_text()
    raw_head = re.sub('\n+','\n', raw_head)
    header = '\t'.join(raw_head.strip('\n').split('\n')[1:]) ##
    print(header, file = out)
    for results_number in range(1,11):
        raw_line = table.find(ind = results_number).get_text()
        raw_line = re.sub('\n+','\n', raw_line)
        # E value 和 identity 列错位
        temp = raw_line.strip('\n').split('\n')
        mismatch = temp[5]
        del temp[5]
        del temp[0]
        temp.insert(5,mismatch[:-6])
        temp.insert(6,mismatch[-6:])
        line = '\t'.join(temp)
        print(line, file = out)
out.close() ## 一定要关闭... 不然输出文件会不全....

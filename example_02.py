'''
requests + lxml + Xpath + csv + re
使用xpath提取http://seputu.com/中盗墓笔记的标题，章节名称和链接,并存储在本地的csv文件中
'''
import csv
import re
import requests
from lxml import etree


#获取网页内容
key = {'User_agent':'Mozilla/4.0'}
r = requests.get('http://seputu.com/',headers = key)
#使用lxml解析网页
html = etree.HTML(r.text)
#先找到所有div class = mulu标记
div_mulus = html.xpath('.//*[@class = "mulu"]')
rows = []
for div_mulu in div_mulus:
    #找到所有div_h2标记
    div_h2 = div_mulu.xpath('./div[@class = "mulu-title"]/center/h2/text()')
    if len(div_h2) > 0:
        h2_title = div_h2[0].encode('utf-8')
        a_s = div_mulu.xpath('./div[@class = "box"]/ul/li/a')
        for a in a_s:
            #找到href属性
            href = a.xpath('./@href')[0].encode('utf-8')
            #找到title属性
            box_title = a.xpath('./@title')[0]
            print(box_title)
            #清洗数据
            pattern = re.compile(r'\s*\[(.*)\]\s+(.*)')
            result = re.search(pattern,'box_title')
            print(result)
            if result != None:
                date = result.group(1).encode('utf-8')
                real_title = result.group(2).encode('utf-8')
                #输出清洗后的标题
                content = (h2_title,real_title,href,date)
                rows.append(content)
    headers = ['title','real_title','href','date']
    with open('盗墓笔记.csv','w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
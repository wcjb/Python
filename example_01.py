'''
reuqets + BeautifulSoup + json 
爬取http://seputu.com/中盗墓笔记的标题，章节，章节名称和链接,并存储在本地的json文件中
'''
import requests
from bs4 import BeautifulSoup
import os
import json

def gethtml(url):
    '''
    获得网页内容
    '''
    try:
        key = {'User_agent':'Mozilla/4.0'}
        r = requests.get(url,headers = key)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return  r.text
    except:
        print('网络异常，爬取失败')

def solution(html):
    '''
    解析网页内容
    并将链接和标题放在字典中
    '''
    content = []
    try:
        soup = BeautifulSoup(html,'html.parser')
        for mulu in soup.find_all(class_ = 'mulu'):
            h2 = mulu.find('h2')
            lists = []
            if h2 != None:
                for a in mulu.find(class_ = 'box').find_all('a'):
                    href = a.get('href')
                    box_title = a.get('title')
                    lists.append({'href':href,'box_title':box_title})
                content.append({'title':h2.string,'content':lists})
        return content
    except:
      print('解析出错！')

def savejson(lists):
    '''
    将解析出的内容保存为json
    '''
    root = "C://Users//wcjb//Desktop//盗墓笔记//"
    path = root + "盗墓笔记" + ".json"
    
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        with open(path,'w') as file:
            json.dump(lists,fp = file,ensure_ascii=False,indent = 4)
            print('数据文件创建成功！')

def main():
    lists = []
    url = 'http://seputu.com'
    html = gethtml(url)
    lists = solution(html)
    savejson(lists)
main()

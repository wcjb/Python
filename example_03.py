'''
使用urlretrieve()下载远程数据到当前目录
'''
import urllib
from lxml import etree
import requests

def Schedule(blocknum,blocksize,totalsize):
    '''
    blocknum:已经下载的数据块
    blocksize：数据块大小
    titalsize：远程文件的大小
    '''
    per = 100.0*blocknum*blocksize/totalsize
    if per > 100:
        per = 100
    print('当前下载进度：%d'%per)

def GetHTML(url):
    '''
    获得目标网址的内容
    url:网页地址
    '''
    try:
        key = {'User-Agent':'Chrome/62.0.3202.62'}
        r = requests.get(url,headers = key)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("网页获取异常！")

def DownLoad(response):
    '''
    解析并下载网页上的图片
    response:获得的网页内容
    '''
    #使用lxml解析网页
    html = etree.HTML(response)
    #先找到所有img
    img_urls = html.xpath('.//img/@src')
    i = 0
    for img_url in img_urls:
        #？无法直接使用urllib.urlretrieve()进行下载
        urllib.request.urlretrieve(img_url,'img'+str(i)+'.jpg',Schedule)
        i += 1
def main():
    url = 'http://www.ivsky.com/tupian/ziranfengguang/'
    response = GetHTML(url)
    DownLoad(response)
main()

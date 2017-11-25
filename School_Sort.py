import  requests
from bs4 import BeautifulSoup
import bs4

def GetHtmlText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding  = r.apparent_encoding
        return r.text
    except:
        return ""
    
def FillUnivList(ulist,html):
    soup = BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children:
        #检测tr标签的类型
        if isinstance(tr,bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string,tds[1].string,tds[3].string])
        
def PrintUnivList(ulist,num):
    string = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(string.format("排名","学校名称","总分",chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(string.format(i,u[1],u[2],chr(12288)))

def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html'
    html = GetHtmlText(url)
    FillUnivList(uinfo,html)
    PrintUnivList(uinfo,100)  
main()
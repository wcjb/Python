import requests
from bs4 import BeautifulSoup
import re
import codecs
import pdfkit
from PyPDF2 import PdfFileMerger
import os
import time


def geturl(firsturl):
    """
    通过入口URL解析所有教程的URL
    :return:待爬取的url列表
    """
    params = {}
    urls = []
    for item in [(3-i) for i in range(3)]:
        params['page'] = item
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/63.0.3239.108 Safari/537.36'}
        try:
            response = requests.get(firsturl, params=params, headers=head)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # [::-1]利用列表的切片操作将列表倒序输出
            links = soup.find_all('a', id=re.compile(r'PostsList1_rpPosts_TitleUrl_\d'))[::-1]
            for link in links:
                urls.append(link['href'])
        except:
            print('Error：!')
    return urls


def parser(url, htmlname):
    """
    从传入的url中解析处文章的标题和正文，并保存在一个html文件中
    :param url: 文章的链接地址
    :param htmlname: 用来保存内容的html文件的名称
    :return: None
    """
    web = {}
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/63.0.3239.108 Safari/537.36'}
    try:
        response = requests.get(url, headers=head)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # 获取正文标题
        web['title'] = soup.find_all('a', id='cb_post_title_url')[0].string
        # 获取正文内容
        web['text'] = soup.find_all(class_="blogpost-body")[0]
        # 将正文的标题和内容保存在一个html文件中
        output_html(htmlname, web)
    except:
        print("Error:解析出错!")


def output_html(htmlname, list):
    """
    将传入的字典中的内容保存在html文件中
    :param htmlname:用来保存内容的html文件的名称
    :param list:保存文章标题和内容
    :return:None
    """
    fout = codecs.open(htmlname, 'w', encoding='utf-8')
    fout.write('<html>')
    fout.write("<head><meta charset='utf-8'/></head>")
    fout.write('<body>')
    fout.write('<h2>%s</h2>' % list['title'])
    fout.write('%s' % list['text'])
    fout.write('</body>')
    fout.write('</html>')
    fout.close()


def save_pdf(html, pdfname):
    """
    把所有html文件保存到pdf文件
    :param html:  html文件
    :param pdfname: pdf文件
    :return:None
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    # 若未将wkhtmltopdf的安装目录添加到系统目录中，则需指定其安装位置
    config = pdfkit.configuration(wkhtmltopdf='D:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # 将html转换为padname
    pdfkit.from_file(html, pdfname, options=options, configuration=config)


def spider():
    """
    主程序，调用相关模块
    :return: None
    """
    start = time.time()
    # 入口URL
    firsturl = 'http://www.cnblogs.com/xdp-gacl/tag/JavaWeb学习总结/default.html'
    sign = 0
    pdfs = []
    htmls = []
    urls = geturl(firsturl)
    for url in urls:
        str1 = str(sign) + '.html'
        str2 = str(sign) + '.pdf'
        parser(url, str1)
        htmls.append(str1)
        pdfs.append(str2)
        save_pdf(str1, str2)
        sign += 1
        print('>>%.2f%%' % (100 * sign / len(urls)))
    print('解析已完成，接下来进行PDF文档的合并！')
    # 进行pdf的合并
    merger = PdfFileMerger()
    for pdf in pdfs:
        file = open(pdf, 'rb')
        merger.append(file)
        file.close()
    output = open('JavaWeb学习总结.pdf', 'wb')
    merger.write(output)
    print("PDF合并已完成！")

    # 删除临时文件
    for html in htmls:
        os.remove(html)
        print('删除临时文件！' + html)
    for pdf in pdfs:
        os.remove(pdf)
        print('删除临时文件！' + pdf)

    total_time = time.time() - start
    print("总共耗时：%f 秒" % total_time)


spider()
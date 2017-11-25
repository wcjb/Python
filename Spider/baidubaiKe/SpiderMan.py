from firstSpider import DataOutput
from firstSpider import HtmlDownloader
from firstSpider import HtmlParser
from firstSpider import UrlManager
from firstSpider import Email


class SpiderMan(object):

    def __init__(self):
        self.manager = UrlManager.UrlManager()
        self.downloader = HtmlDownloader.HtmlDownloader()
        self.parser = HtmlParser.HtmlParser()
        self.output = DataOutput.DataOutput()
        self.email = Email.Email()

    def crawl(self, root_url):
        # 添加入口URL
        self.manager.add_new_url(root_url)

        # 判断url管理器中是否有新的url，同时判断抓取了多少个url
        while self.manager.has_new_url() and self.manager.old_url_size() < 500:
            try:
                # 从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                # 从HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页数据
                new_urls, data = self.parser.parser(new_url, html)
                # 将抽取的url添加到URL管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储器存储文件
                self.output.store_data(data)
                print("已抓取%s个链接" % self.manager.old_url_size())
            except:
                print('crawl failed')

        self.output.output_html()
        self.email.eamil(1)


if __name__ == "__main__":
    spider_man = SpiderMan()
    spider_man.crawl("http://baike.baidu.com/item/%E8%9C%98%E8%9B%9B/8135707")

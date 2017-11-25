import requests


class HtmlDownloader(object):

    @staticmethod
    def download(url):
        if url is None:
            return None
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            return response.text
        except:
            return None

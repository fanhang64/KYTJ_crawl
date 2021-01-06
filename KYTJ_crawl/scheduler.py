
from KYTJ_crawl.crawler import Crawler
from KYTJ_crawl.api import app
from KYTJ_crawl.settings import API_HOST, API_PORT, API_ENABLED


class Schedule:
    def __init__(self):
        self.crawler = Crawler()
    
    def api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        
        # 获取
        self.crawler.run()

        # api
        if API_ENABLED:
            self.api()

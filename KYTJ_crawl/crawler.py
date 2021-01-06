from urllib.parse import urljoin

from lxml import etree

from .utils import get_text, check_list
from .settings import TJ_YEAR


class CrawlerMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(metaclass=CrawlerMetaClass):
    def get_items(self, callback):
        items = []
        for item in eval("self.{}()".format(callback)):
            print('成功获取学校信息', item)
            items.append(item)
        return items

    def crawl_chinakaoyan(self):

        base_url = "http://www.chinakaoyan.com/"
        url = "{}tiaoji/schoollist/pagenum/{}.shtml"

        for i in range(1, 2):
            items = []
            total_url = url.format(base_url, i)
            res_text = get_text(total_url)
            if res_text:
                html = etree.HTML(res_text)
                div_list = html.xpath("//div/div[@class='info-item font14']")
                for x in div_list:
                    published_date=check_list(x.xpath("./span[4]/text()"))
                    year = published_date.split("-")[0]
                    if year and int(year) < TJ_YEAR:
                        break   # 网站按时间排序逆序排序

                    url = check_list(x.xpath("./span[3]/a/@href"))
                    if url:
                        url = urljoin(base_url, url)

                    item = dict(
                        university_name=check_list(x.xpath("./span[1]/text()")),
                        major=check_list(x.xpath("./span[2]/text()")),
                        neirong=check_list(x.xpath("./span[3]/a/@title")),
                        published_date=published_date,
                        url=url
                    )

                    yield item 

    def crawl_muchong(self):
        return []

        
    def run(self):
        print('获取器开始执行')
        for callback_label in range(self.__CrawlFuncCount__):
            callback = self.__CrawlFunc__[callback_label]
            # 获取
            items = self.get_items(callback)

            # save2db

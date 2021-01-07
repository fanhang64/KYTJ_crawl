from urllib.parse import urljoin

from lxml import etree

from .utils import get_text, check_list, get_md5
from .settings import TJ_YEAR
from .db import university_db


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
            print('成功获取学校信息:', item)
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
                        break   # TODO 网站按时间排序逆序排序

                    url = check_list(x.xpath("./span[3]/a/@href"))
                    if url:
                        url = urljoin(base_url, url)

                    item = dict(
                        university_name=check_list(x.xpath("./span[1]/text()")),
                        major=check_list(x.xpath("./span[2]/text()")),
                        neirong=check_list(x.xpath("./span[3]/a/@title")),
                        published_date=published_date,
                        url=url,
                    )

                    uid = get_md5(item)
                    item['uid'] = uid
                    yield item 

    def crawl_muchong(self):
        base_url = "http://muchong.com/"
        url = "/bbs/kaoyan.php?action=adjust&type=1&page={}"

        for i in range(1, 2):
            total_url = urljoin(base_url, url.format(i))

            res_text = get_text(total_url)
            if res_text:
                html = etree.HTML(res_text)
                tr_list = html.xpath("//div[@class='wrapper'][1]/table/tbody[@class='forum_body_manage']/tr")
                for tr in tr_list:
                    published_date=check_list(tr.xpath("./td[5]/text()"))
                    year = published_date.split("-")[0]
                    # if year and int(year) < TJ_YEAR:
                    #     break # TODO
                    neirong = check_list(tr.xpath("./td[1]/a/text()"))
                    num = check_list(tr.xpath("./td[4]/text()"))
                    if num and int(num):
                        neirong = neirong + " 招生人数：{}".format(num)

                    item = dict(
                        university_name=check_list(tr.xpath("./td[2]/text()")),
                        major=check_list(tr.xpath("./td[3]/text()")),
                        neirong=neirong,
                        url=check_list(tr.xpath("./td[1]/a/@href")),
                        published_date=published_date.split(" ")[0]
                    )
                    uid = get_md5(item)
                    item['uid'] = uid
                    yield item
        
    def run(self):
        print('获取器开始执行')
        for callback_label in range(self.__CrawlFuncCount__):
            callback = self.__CrawlFunc__[callback_label]
            # 获取
            items = self.get_items(callback)

            # save2db
            university_db.save2db(items)

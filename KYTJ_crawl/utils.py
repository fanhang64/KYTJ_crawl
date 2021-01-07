import functools
import time
import hashlib

import requests
from requests import ConnectionError


base_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/14.04.6 Chrome/81.0.3990.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def check_list(obj):
    return obj[0] if obj and isinstance(obj, list) else ""


def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_times = 0
            while retry_times < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retry_times += 1
                    print(e)
        return wrapper
    return decorator


@retry(2)
def get_text(url, **other_herders):
    headers = dict(base_headers, **other_herders)

    try:
        res = requests.get(url, headers=headers)
        print("抓取成功：", url, res.status_code)
        if res.status_code == 200:
            return res.text
    except ConnectionError:
        print("抓取失败", url)


def get_md5(obj:dict):
    """
        用于内容去重
        obj: 为一条学校信息记录
    """

    input_text = hashlib.md5()
    xx = "%s-%s-%s" % (obj['university_name'],obj['major'], obj['neirong'])
    input_text.update(xx.encode("utf-8"))
    return input_text.hexdigest()

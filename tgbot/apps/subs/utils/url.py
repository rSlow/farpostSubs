import re

from fake_useragent import UserAgent


def get_headers():
    return {
        "Accept": "text/html,"
                  "application/xhtml+xml,"
                  "application/xml;q=0.9,"
                  "image/avif,"
                  "image/webp,"
                  "image/apng,"
                  "*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent().random
    }


def prepare_url(url: str):
    str_url = re.sub(re.compile(r"#.*"), "", url)
    str_url = re.sub(re.compile(r"date_created_min=[0-9]*"), "", str_url)
    str_url = re.sub(re.compile(r"search_id=[0-9]*"), "", str_url)
    str_url = re.sub(re.compile(r"&$"), "", str_url)
    str_url = str_url.replace("&&", "&")
    return str_url

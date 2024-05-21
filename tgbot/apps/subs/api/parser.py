from bs4 import BeautifulSoup


def is_valid_url(data: bytes | str):
    soup = BeautifulSoup(data, "html.parser")
    ads_table = soup.select("table.viewdirBulletinTable")
    return bool(ads_table)


def get_new_ads_list(data: bytes | str):
    soup = BeautifulSoup(data, "html.parser")
    return soup.select("*[data-accuracy=sse-bulletin-new]")

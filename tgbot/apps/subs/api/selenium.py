from selenium.webdriver.remote.webdriver import WebDriver

from common.utils.decorators import to_async_thread


@to_async_thread
def download_page(url: str, webdriver: WebDriver):
    webdriver.get(url)
    webdriver.implicitly_wait(10)
    page_data = webdriver.page_source
    return page_data

import re

from common.filters import regexp_factory

URLPattern = re.compile(r"https?://(www\.)?farpost\.ru/saved_search/[A-Za-z0-9]+/[0-9]+/show")

farpost_url_factory = regexp_factory(
    pattern=URLPattern,
    error_message="Неверная ссылка: {value}"
)

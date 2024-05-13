from datetime import datetime


def as_strftime(dt: datetime):
    return dt.strftime('%d-%m-%Y %H:%M:%S')

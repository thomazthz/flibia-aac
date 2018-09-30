import datetime


def pretty_datetime(date_format):
    def _pretty_date(timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime(date_format)
    return _pretty_date

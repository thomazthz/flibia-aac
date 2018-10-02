import arrow
from flask import current_app

from .extensions import mail


def pretty_datetime(date_format):
    def _pretty_date(timestamp):
        dt = arrow.get(timestamp)
        return dt.format(date_format)
    return _pretty_date


def now():
    return arrow.now(current_app.config['TIME_ZONE'])


def send_mail(email, subject, body):
    mail.send_message(
        subject,
        recipients=[email],
        html=body
    )

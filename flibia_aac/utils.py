from importlib import import_module

import arrow
from flask import current_app


def pretty_datetime(date_format):
    def _pretty_date(timestamp):
        dt = arrow.get(timestamp)
        return dt.format(date_format)
    return _pretty_date


def now():
    return arrow.now(current_app.config['TIME_ZONE'])


def send_mail(email, subject, body):
    mail = current_app.extensions['mail']
    mail.send_message(
        subject,
        recipients=[email],
        html=body
    )


def import_string(dotted_path):
    """ Borrowed from django/utils/module_loading.py
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err

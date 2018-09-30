from flibia_aac.utils import pretty_datetime


def configure(app):
    app.jinja_env.filters['pretty_datetime'] = pretty_datetime(app.config['FULL_DATETIME_FORMAT'])
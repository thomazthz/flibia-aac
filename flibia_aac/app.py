import os

from flask import Flask

from .db import db
from .extensions import csrf, login_manager, mail
from .settings import get_config_object


def create_app(config_name=None, test=False):
    app = Flask(__name__)

    config_name = config_name or os.getenv('FLASK_ENV', 'development')

    app.config.from_object(get_config_object(config_name))

    app.template_folder = 'templates/{}'.format(app.config['THEME_NAME'])
    app.static_folder = 'static/{}'.format(app.config['THEME_NAME'])

    register_blueprints(app)
    register_database(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    from flibia_aac.core.views import core
    app.register_blueprint(core)
    from flibia_aac.accounts.views import account
    app.register_blueprint(account)
    from flibia_aac.players.views import player
    app.register_blueprint(player)


def register_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'account.login'

    @login_manager.user_loader
    def user_loader(account_id):
        from flibia_aac.accounts.models import Account
        return Account.query.get(account_id)


def register_database(app):
    db.init_app(app)


def register_extensions(app):
    from flibia_aac.template_filters import configure
    configure(app)

    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

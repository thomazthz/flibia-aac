from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from flibia_aac.flask_widgets import Widgets

csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()
widgets = Widgets()

login_manager.login_view = 'account.login'


@login_manager.user_loader
def user_loader(account_id):
    from flibia_aac.accounts.models import Account
    return Account.query.get(account_id)

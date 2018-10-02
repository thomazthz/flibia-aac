from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'account.login'

@login_manager.user_loader
def user_loader(account_id):
    from flibia_aac.accounts.models import Account
    return Account.query.get(account_id)

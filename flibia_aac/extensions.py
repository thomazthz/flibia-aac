from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager


csrf = CSRFProtect()
login_manager = LoginManager()


login_manager.login_view = 'account.login'

@login_manager.user_loader
def user_loader(account_id):
    from flibia_aac.accounts.models import Account
    return Account.query.get(account_id)
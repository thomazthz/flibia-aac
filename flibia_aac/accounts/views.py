from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flask_login import current_user

from ..db import db
from ..players.forms import CharacterCreationForm
from ..security import check_password, generate_hash_password

from .forms import LoginForm, RegistrationForm
from .models import Account

account = Blueprint('account', __name__)


@account.route('/my_account', methods=['GET'])
@login_required
def detail():
    acc = current_user
    return render_template('accounts/my_account.html', account=acc, char_creation_form=CharacterCreationForm())


@account.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    char_form = CharacterCreationForm()

    # TODO validate char_form
    # TODO create character
    # TODO success message

    if form.validate_on_submit():
        acc = Account(name=form.name.data,
                      password=generate_hash_password(form.password.data))
        db.session.add(acc)
        db.session.commit()

        return redirect(url_for('account.login'))

    return render_template('accounts/register.html', form=form, char_form=char_form)


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        acc = Account.query.filter_by(name=form.name.data).first()

        if not acc or not check_password(acc.password, form.password.data):
            form.errors['name'] = ['Invalid account name or password']
        else:
            login_user(acc)
            return redirect(url_for('account.detail'))

    return render_template('accounts/login.html', form=form)


@account.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

import time

from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import (current_user, fresh_login_required, login_required,
                         login_user, logout_user)

from ..db import db
from ..players.forms import CharacterCreationForm
from ..security import (check_confirmed, check_password,
                        confirm_email_confirmation_token,
                        generate_confirmation_token, generate_hash_password)
from ..utils import now, send_mail
from .forms import LoginForm, RegistrationForm
from .models import Account

account = Blueprint('account', __name__)


@account.route('/my_account', methods=['GET'])
@login_required
@check_confirmed
def detail():
    acc = current_user
    return render_template('accounts/my_account.html', account=acc, char_creation_form=CharacterCreationForm())


@account.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    char_form = CharacterCreationForm()

    # TODO validate char_form
    # TODO create character

    if form.validate_on_submit():
        acc = Account(name=form.name.data,
                      email=form.email.data,
                      password=generate_hash_password(form.password.data))

        db.session.add(acc)
        db.session.commit()

        token = generate_confirmation_token(acc.email)

        url = url_for('account.email_confirmation', token=token, _external=True)

        email_body = render_template('email/confirmation.html', url=url)

        send_mail(acc.email, 'Confirm your email', email_body)

        flash('Email verification required.', 'warning')
        flash('We have sent you an email with an activation link '
              'to your submitted email address.', 'message')

        login_user(acc)

        return redirect(url_for('account.login'))

    return render_template('accounts/register.html', form=form, char_form=char_form)


@account.route('/register/confirmation/<string:token>', methods=['GET'])
def email_confirmation(token):
    email = confirm_email_confirmation_token(token)

    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('core.index'))

    acc = Account.query.filter_by(email=email).first()

    if acc.creation:
        flash('Account already confirmed. Please login.', 'success')
    else:
        acc.creation = now().timestamp
        db.session.add(acc)
        db.session.commit()
        flash('You have confirmed your email. You can login now', 'success')

    return redirect(url_for('account.login'))


@account.route('/register/unconfirmed', methods=['GET'])
@login_required
def unconfirmed():
    if current_user.creation:
        return redirect(url_for('account.detail'))
    return render_template('accounts/unconfirmed.html')


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        acc = Account.query.filter_by(name=form.name.data).first()

        if acc and check_password(acc.password, form.password.data):
            login_user(acc)
            return redirect(url_for('account.detail'))
        else:
            form.errors['name'] = ['Invalid account name or password']
    return render_template('accounts/login.html', form=form)


@account.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

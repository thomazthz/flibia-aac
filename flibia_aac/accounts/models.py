import time
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGBLOB, SMALLINT, TINYINT

from flask_login import UserMixin

from ..db import db
from ..players.models import Player


class Account(UserMixin, db.Model):
    __tablename__ = 'accounts'

    id = db.Column(INTEGER(11), primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    secret = db.Column(db.CHAR(16))
    type = db.Column(INTEGER(11), nullable=False, server_default=db.text("'1'"))
    premdays = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    lastday = db.Column(INTEGER(10), nullable=False, server_default=db.text("'0'"))
    email = db.Column(db.String(255), nullable=False, server_default=db.text("''"))
    creation = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))


class AccountBan(Account):
    __tablename__ = 'account_bans'

    account_id = db.Column(db.ForeignKey('accounts.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    reason = db.Column(db.String(255), nullable=False)
    banned_at = db.Column(BIGINT(20), nullable=False)
    expires_at = db.Column(BIGINT(20), nullable=False)
    banned_by = db.Column(db.ForeignKey('players.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    player = db.relationship(Player)
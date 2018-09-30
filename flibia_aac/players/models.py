from enum import Enum

from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGBLOB, SMALLINT, TINYINT

from ..db import db


class Vocation(Enum):
    NONE = 0
    SORCERER = 1
    DRUID = 2
    PALADIN = 3
    KNIGHT = 4
    MASTER_SORCERER = 5
    ELDER_DRUID = 6
    ROYAL_PALADIN = 7
    ELITE_KNIGHT = 8


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(INTEGER(11), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    group_id = db.Column(INTEGER(11), nullable=False, server_default=db.text("'1'"))
    account_id = db.Column(db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, index=True, server_default=db.text("'0'"))
    level = db.Column(INTEGER(11), nullable=False, server_default=db.text("'1'"))
    vocation = db.Column(INTEGER(11), nullable=False, index=True, server_default=db.text("'0'"))
    health = db.Column(INTEGER(11), nullable=False, server_default=db.text("'150'"))
    healthmax = db.Column(INTEGER(11), nullable=False, server_default=db.text("'150'"))
    experience = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    lookbody = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    lookfeet = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    lookhead = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    looklegs = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    looktype = db.Column(INTEGER(11), nullable=False, server_default=db.text("'136'"))
    lookaddons = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    maglevel = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    mana = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    manamax = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    manaspent = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    soul = db.Column(INTEGER(10), nullable=False, server_default=db.text("'0'"))
    town_id = db.Column(INTEGER(11), nullable=False, server_default=db.text("'1'"))
    posx = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    posy = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    posz = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    conditions = db.Column(db.LargeBinary, nullable=False)
    cap = db.Column(INTEGER(11), nullable=False, server_default=db.text("'400'"))
    sex = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    lastlogin = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    lastip = db.Column(INTEGER(10), nullable=False, server_default=db.text("'0'"))
    save = db.Column(TINYINT(1), nullable=False, server_default=db.text("'1'"))
    skull = db.Column(TINYINT(1), nullable=False, server_default=db.text("'0'"))
    skulltime = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    lastlogout = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    blessings = db.Column(TINYINT(2), nullable=False, server_default=db.text("'0'"))
    onlinetime = db.Column(INTEGER(11), nullable=False, server_default=db.text("'0'"))
    deletion = db.Column(BIGINT(15), nullable=False, server_default=db.text("'0'"))
    balance = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    offlinetraining_time = db.Column(SMALLINT(5), nullable=False, server_default=db.text("'43200'"))
    offlinetraining_skill = db.Column(INTEGER(11), nullable=False, server_default=db.text("'-1'"))
    stamina = db.Column(SMALLINT(5), nullable=False, server_default=db.text("'2520'"))
    skill_fist = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_fist_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    skill_club = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_club_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    skill_sword = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_sword_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    skill_axe = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_axe_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    skill_dist = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_dist_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    skill_shielding = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_shielding_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    skill_fishing = db.Column(INTEGER(10), nullable=False, server_default=db.text("'10'"))
    skill_fishing_tries = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))

    account = db.relationship('Account', backref=db.backref('characters', lazy=True))


class PlayerDeaths(db.Model):
    __tablename__ = 'player_deaths'

    player_id = db.Column(db.ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    player = db.relationship('Player', foreign_keys=[player_id], viewonly=True, backref=db.backref('deaths'))
    time = db.Column(BIGINT(20), nullable=False, server_default=db.text("'0'"))
    level = db.Column(INTEGER(11), nullable=False, server_default=db.text("'1'"))
    killed_by = db.Column(db.String(255), nullable=False, index=True)
    is_player = db.Column(TINYINT(1), nullable=False, server_default=db.text("'1'"))
    mostdamage_by = db.Column(db.String(100), nullable=False, index=True)
    mostdamage_is_player = db.Column(TINYINT(1), nullable=False, server_default=db.text("'0'"))
    unjustified = db.Column(TINYINT(1), nullable=False, server_default=db.text("'0'"))
    mostdamage_unjustified = db.Column(TINYINT(1), nullable=False, server_default=db.text("'0'"))


class PlayersOnline(db.Model):
    __tablename__ = 'players_online'

    player_id = db.Column(INTEGER(11), primary_key=True)

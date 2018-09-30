from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask.views import MethodView

from flask_login import current_user, login_required, login_user, logout_user

from sqlalchemy import or_
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy.sql import func

from ..db import db

from .forms import CharacterCreationForm, SearchForm
from .models import Player, PlayersOnline, PlayerDeaths, Vocation

player = Blueprint('player', __name__, url_prefix='/character')


def _vocation_filter_builder(vocation, promoted_vocation=None):
    if not promoted_vocation:
        return Player.vocation==Vocation[vocation].value
    return or_(Player.vocation==Vocation[vocation].value,
               Player.vocation==Vocation[promoted_vocation].value)

HIGHSCORES_CATEGORIES = {
    'experience': 'experience',
    'magic_level': 'maglevel',
    'fist': 'skill_fist',
    'club': 'skill_club',
    'sword': 'skill_sword',
    'axe': 'skill_axe',
    'dist': 'skill_dist',
    'shielding': 'skill_shielding',
    'fishing': 'skill_fishing',
}

VOCATIONS_FILTERS = {
    'sorcerer': _vocation_filter_builder('SORCERER', 'MASTER_SORCERER'),
    'druid': _vocation_filter_builder('DRUID', 'ELDER_DRUID'),
    'paladin': _vocation_filter_builder('PALADIN', 'ROYAL_PALADIN'),
    'knight': _vocation_filter_builder('KNIGHT', 'ELITE_KNIGHT'),
    'rookie': _vocation_filter_builder('NONE'),
    'all': None,
}


@player.route('/create', methods=['GET', 'POST'])
@login_required
def create_character():
    form = CharacterCreationForm()
    if form.validate_on_submit():
        player = Player(name=form.name.data,
                        sex=int(form.sex.data),
                        conditions='-1'.encode('ascii'),
                        account=current_user)
        db.session.add(player)
        db.session.commit()
    return redirect(url_for('account.detail'))



@player.route('/profile', methods=['GET'])
def profile():
    form = SearchForm()
    name = request.args.get('name', None)

    player = Player.query.filter_by(name=name).first()

    return render_template('players/profile.html', form=form, player=player)


@player.route('/highscores', methods=['GET', 'POST'])
def highscores():
    highscore_category = request.args.get('highscore_category', 'experience')
    vocation_filter = request.args.get('vocation', None)

    highscore_category = HIGHSCORES_CATEGORIES.get(highscore_category)
    vocation_filter = VOCATIONS_FILTERS.get(vocation_filter, None)

    field = getattr(Player, highscore_category)
    players = Player.query.options(load_only(field))

    if vocation_filter is not None:
        players = players.filter(vocation_filter)

    return render_template('players/highscores.html', players=players, highscore_category=highscore_category)


@player.route('/players_online', methods=['GET'])
def players_online():
    players_count = db.session.query(func.count(PlayersOnline.player_id)).scalar()
    players = db.session.query(Player.name, Player.level, Player.vocation) \
                        .filter(Player.id==PlayersOnline.player_id).all()
    return render_template('players/players_online.html', players=players, players_count=players_count)


@player.route('/latest_deaths', methods=['GET'])
def latest_deaths():
    deaths = db.session.query(PlayerDeaths) \
               .options(joinedload(PlayerDeaths.player, innerjoin=True). \
                        load_only('name')).limit(100).all()

    return render_template('players/latest_deaths.html', deaths=deaths)

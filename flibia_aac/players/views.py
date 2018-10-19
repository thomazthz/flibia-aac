from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask.views import MethodView

from flask_login import current_user, login_required, login_user, logout_user

from sqlalchemy import or_
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy.sql import func

from flibia_aac.db import db
from flibia_aac.queries import get_highscores

from .forms import CharacterCreationForm, SearchForm
from .models import Player, PlayersOnline, PlayerDeaths


player = Blueprint('player', __name__, url_prefix='/character')


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
    category = request.args.get('highscore_category', 'experience')
    vocation = request.args.get('vocation', None)

    players = get_highscores(category, vocation)

    return render_template('players/highscores.html',
                           players=players,
                           highscore_category=category)


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

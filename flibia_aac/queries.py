from sqlalchemy import or_
from sqlalchemy.orm import load_only

from .players.models import Player, Vocation


def _vocation_filter_builder(vocation, promoted_vocation=None):
    if not promoted_vocation:
        return Player.vocation==Vocation[vocation].value
    return or_(Player.vocation==Vocation[vocation].value,
               Player.vocation==Vocation[promoted_vocation].value)


VOCATIONS_FILTERS = {
    'sorcerer': _vocation_filter_builder('SORCERER', 'MASTER_SORCERER'),
    'druid': _vocation_filter_builder('DRUID', 'ELDER_DRUID'),
    'paladin': _vocation_filter_builder('PALADIN', 'ROYAL_PALADIN'),
    'knight': _vocation_filter_builder('KNIGHT', 'ELITE_KNIGHT'),
    'rookie': _vocation_filter_builder('NONE'),
    'all': None,
}


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


def get_highscores(category, vocation=None, limit=None):
    highscore_category = HIGHSCORES_CATEGORIES.get(category)
    vocation_filter = VOCATIONS_FILTERS.get(vocation, None)

    field = getattr(Player, highscore_category)
    players = Player.query.options(load_only(field))

    if vocation_filter is not None:
        players = players.filter(vocation_filter)

    if limit:
        players = players.limit(limit)

    return players

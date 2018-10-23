from flask import render_template

from flibia_aac.flask_widgets import Widget
from flibia_aac.queries import get_highscores, get_players_online_count


class TopExperienceWidget(Widget):
    name = 'top_experience'

    def render(self):
        players = get_highscores('experience', limit=10)
        return render_template('widgets/top_experience.html', players=players)


class PlayersOnlineWidget(Widget):
    name = 'players_online'

    def render(self):
        players_online = get_players_online_count()
        return render_template('widgets/players_online.html', players_online=players_online)

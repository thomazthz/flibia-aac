from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)


core = Blueprint('core', __name__)

@core.route('/', methods=['GET'])
def index():
    return render_template('index.html')

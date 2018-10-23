from abc import ABC

from flask import Markup

from .utils import import_string


class Widget(ABC):
    name = ''
    escape = True

    def render():
        raise NotImplementedError


class Widgets:
    def __init__(self, app=None):
        self.app = app
        self.widgets = {}

        if app:
            self.init_app(app)

    def init_app(self, app):
        app.widgets = self

        self.active_widgets = app.config.get('ACTIVE_WIDGETS', None)

        self.load_widgets()

        app.jinja_env.globals['widgets'] = self

    def load_widgets(self):
        if not self.active_widgets:
            # print('No widgets specified in settings')
            return

        for widget_path in self.active_widgets:
            # print('Importing {}'.format(widget_path))

            widget_cls = import_string(widget_path)

            widget = widget_cls()

            if not widget.name:
                raise ValueError('Missing Widget name in {}'.format(widget_cls))

            if widget.name in self.widgets.keys():
                raise ValueError('Widget name must be unique. '
                                 'Duplicated name {}'.format(widget.name))

            self.widgets[widget.name] = widget

    def __call__(self, widget_name):
        if widget_name not in self.widgets.keys():
            raise ValueError(
                '{} is not a valid/registered Widget'.format(widget_name)
            )
        widget = self.widgets[widget_name]
        response = widget.render()
        if widget.escape:
            response = Markup(response)
        return response

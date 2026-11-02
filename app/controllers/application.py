import os
from bottle import template, TEMPLATE_PATH

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
views_path = os.path.join(BASE_DIR, 'app', 'views', 'html')
if views_path not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, views_path)
if BASE_DIR not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, BASE_DIR)


class Application():

    def __init__(self):
        self.pages = {
            'despesas': self.despesas,
            'helper': self.helper
        }

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def despesas(self):
        return template('despesas')

    def helper(self):
        return template('helper')

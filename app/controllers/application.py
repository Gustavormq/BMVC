from bottle import template


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
        return template('app/views/html/despesas')

    def helper(self):
        return template('app/views/html/helper')

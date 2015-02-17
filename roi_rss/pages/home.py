import webapp2

from roi_rss import utils

class Home(webapp2.RequestHandler):
    '''Handles homepage requests.'''

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write(utils.render_template('home.html'))

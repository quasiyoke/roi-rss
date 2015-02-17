import os

from google.appengine.ext.webapp import template


APP_DIR = os.path.dirname(__file__)

def render_template(name, context={}):
    return template.render(os.path.join(APP_DIR, 'templates', name), context)

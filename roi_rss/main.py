import os
import webapp2

from . import pages

app = webapp2.WSGIApplication([
    ('/', pages.Home),
], debug = False)

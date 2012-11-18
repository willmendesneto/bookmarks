#!/usr/bin/env python

import os
from google.appengine.ext import webapp
#from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

#from model.Categoria import Categoria
#from model.Coisa import Coisa

#def _template_path(filename):
#    return os.path.join(os.path.dirname(__file__), 'view', filename)

def _render_template(filename, values):
    return template.render(os.path.join(os.path.dirname(__file__), 'view', filename), values)

class LandingPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(_render_template('landing.html', template_values))
    def post(self):
        template_values = {}
        if self.request.get('username') != '':
            self.response.out.write(_render_template('home.html', template_values))
        else:
            self.response.out.write(_render_template('signup.html', template_values))

class PwdRecoverPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(_render_template('pwdrecover.html', template_values))

def main():
    application = webapp.WSGIApplication([('/', LandingPage),
                                            ('/landing.*', LandingPage),
                                            ('/pwdrecover.*', PwdRecoverPage),
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

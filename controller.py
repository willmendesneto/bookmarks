#!/usr/bin/env python

import os
from google.appengine.ext import webapp
#from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

#from model.Categoria import Categoria
#from model.Coisa import Coisa

def _template_path(filename):
    return os.path.join(os.path.dirname(__file__), 'view', filename)

class LandingPage(webapp.RequestHandler):
    def get(self):
        template_values = {}        
        self.response.out.write(template.render(_template_path('landing.html'), template_values))        

def main():
    application = webapp.WSGIApplication([('/', LandingPage), 
                                            ('/landing.*', LandingPage),                                           
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

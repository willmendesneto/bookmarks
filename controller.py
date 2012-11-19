#!/usr/bin/env python

import os
from google.appengine.ext import webapp
#from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
#from string import strip

#from model.Categoria import Categoria
#from model.Coisa import Coisa
from model import *

#def _template_path(filename):
#    return os.path.join(os.path.dirname(__file__), 'view', filename)

def _render_template(filename, values):
    return template.render(os.path.join(os.path.dirname(__file__), 'view', filename), values)

class LandingPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(_render_template('landing.html', template_values))
    def post(self):
        if self.request.get('username').strip() != '':
            self.redirect('/home')
        else:
            errors = []
            if self.request.get('newusername').strip() == '':
                errors.append('blank_newusername')
            if self.request.get('newemail').strip() == '':
                errors.append('blank_newemail')
            if self.request.get('newpassword').strip() == '':
                errors.append('blank_newpassword')
            if self.request.get('newconfirm').strip() == '':
                errors.append('blank_newconfirm')
            if not 'blank_newpassword' in errors and not 'blank_newconfirm' in errors:
                if self.request.get('newpassword').strip() != self.request.get('newconfirm').strip():
                    errors.append('different_passwords')
            if len(errors) == 0:
                query = User.all()
                query.filter('name =', self.request.get('newusername').strip())
                if query.count() > 0:
                    errors.append('username_taken')
            if len(errors) == 0:
                query = User.all()
                query.filter('email =', self.request.get('newemail').strip())
                if query.count() > 0:
                    errors.append('email_taken')
            if len(errors) == 0:
                obj = User(name = self.request.get('newusername').strip(),
                    email = self.request.get('newemail').strip(),
                    password = self.request.get('newpassword').strip(),
                    status = 'new'
                )
                obj.put()
                self.redirect('/home')
            else:
                template_values = {'errors' : errors}
                self.response.out.write(_render_template('landing.html', template_values))

class HomePage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(_render_template('home.html', template_values))

class PwdRecoverPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(_render_template('pwdrecover.html', template_values))

def main():
    application = webapp.WSGIApplication([('/', LandingPage),
                                            ('/landing.*', LandingPage),
                                            ('/home.*', HomePage),
                                            ('/pwdrecover.*', PwdRecoverPage),
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

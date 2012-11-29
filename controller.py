#!/usr/bin/env python

import os
from google.appengine.ext import webapp
#from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
import gmemsess

from model import *

def _render_template(filename, values):
    return template.render(os.path.join(os.path.dirname(__file__), 'view', filename), values)

class LandingPage(webapp.RequestHandler):

    def get(self):
        template_values = {'errors' : [], 'fields' : {} }
        self.response.out.write(_render_template('landing.html', template_values))

    def post(self):
        errors = []
        fields = {
            'username' : self.request.get('username').strip(),
            'newusername' : self.request.get('newusername').strip(),
            'newemail' : self.request.get('newemail').strip()
        }
        if self.request.get('username').strip() != '':
            if self.request.get('password').strip() == '':
                errors.append('blank_password')
            if len(errors) == 0:
                query = User.all()
                query.filter('name =', self.request.get('username').strip())
                if query.count() > 0:
                    obj = query.get()
                    if obj.status != 'active':
                        errors.append('non_active_user')
                    else:    
                        if obj.password != self.request.get('password').strip():
                            errors.append('wrong_password')
                else:
                    errors.append('unknown_username')
            if len(errors) == 0:
                sess = gmemsess.Session(self)
                sess['username'] = self.request.get('username').strip()
                sess.save()
                self.redirect('/home')
            else:
                template_values = {'errors' : errors, 'fields' : fields}
                self.response.out.write(_render_template('landing.html', template_values))
        else:
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
                self.redirect('/signupconf')
            else:
                template_values = {'errors' : errors, 'fields' : fields}
                self.response.out.write(_render_template('landing.html', template_values))

class SignUpConfPage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        self.response.out.write(_render_template('signupconf.html', template_values))

class HomePage(webapp.RequestHandler):

    def get(self):
        sess = gmemsess.Session(self)
        if sess.is_new():
            template_values = {'errors' : ['invalid_session'], 'fields' : {} }
            self.response.out.write(_render_template('landing.html', template_values))
        else:
            bookmarks = []
            tags = []
            template_values = {'username' : sess['username'], 'bookmarks' : bookmarks, 'tags' : tags}
            self.response.out.write(_render_template('home.html', template_values))

    def post(self):
        sess = gmemsess.Session(self)
        if sess.is_new():
            template_values = {'errors' : ['invalid_session'], 'fields' : {} }
            self.response.out.write(_render_template('landing.html', template_values))
        else:        
            errors = []
            fields = {
                'bmark_title' : self.request.get('bmark_title').strip(),
                'bmark_link' : self.request.get('bmark_link').strip(),
                'bmark_tags' : self.request.get('bmark_tags').strip()
            }
            template_values = {'errors' : errors, 'fields' : fields}
            self.response.out.write(_render_template('home.html', template_values))
        
class LogOutCmd(webapp.RequestHandler):

    def get(self):
        sess = gmemsess.Session(self)
        sess.invalidate()
        self.redirect('/landing')

class PwdRecoverPage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        self.response.out.write(_render_template('pwdrecover.html', template_values))

def main():
    application = webapp.WSGIApplication([('/', LandingPage),
                                            ('/landing.*', LandingPage),
                                            ('/signupconf.*', SignUpConfPage),
                                            ('/home.*', HomePage),
                                            ('/logout.*', LogOutCmd),                                            
                                            ('/pwdrecover.*', PwdRecoverPage),
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

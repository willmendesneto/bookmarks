#!/usr/bin/env python

import os
from google.appengine.ext import webapp
#from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
import gmemsess

from model import *

def _renderTemplate(filename, values):
    return template.render(os.path.join(os.path.dirname(__file__), 'view', filename), values)

def _getUserByName(username):
    usr = None
    query = User.all()
    query.filter('name =', username)
    if query.count() > 0:
        usr = query.get()
    return usr

def _getBookmarksByUsername(username):
    usr = None
    query = User.all()
    query.filter('name =', username)
    if query.count() > 0:
        usr = query.get()
    return usr

def _getBookmarksByUserRef(userkey):
    bmks = []
    

class LandingPage(webapp.RequestHandler):

    def get(self):
        template_values = {'errors' : [], 'fields' : {} }
        self.response.out.write(_renderTemplate('landing.html', template_values))

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
                usr = _getUserByName(self.request.get('username').strip())
                if usr:
                    if usr.status != 'active':
                        errors.append('non_active_user')
                    else:    
                        if usr.password != self.request.get('password').strip():
                            errors.append('wrong_password')
                else:
                    errors.append('unknown_username')
            if len(errors) == 0:
                sess = gmemsess.Session(self)
                #sess['username'] = self.request.get('username').strip()
                sess['username'] = usr.name
                sess['userkey'] = usr.key()
                sess.save()
                self.redirect('/home')
            else:
                template_values = {'errors' : errors, 'fields' : fields}
                self.response.out.write(_renderTemplate('landing.html', template_values))
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
                self.response.out.write(_renderTemplate('landing.html', template_values))

class SignUpConfPage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        self.response.out.write(_renderTemplate('signupconf.html', template_values))

class HomePage(webapp.RequestHandler):

    def get(self):
        sess = gmemsess.Session(self)
        if sess.is_new():
            template_values = {'errors' : ['invalid_session'], 'fields' : {} }
            self.response.out.write(_renderTemplate('landing.html', template_values))
        else:            
            #usr = _getUserByName(sess['username'])
            bookmarks = [ b for b in Bookmark.all().filter('user =', sess['userkey']).run() ] # _getBookmarksByUserRef(sess['userkey']) #[]
            tags = [sess['userkey']] # _getTagsByUserRef(sess['userkey'])
            template_values = {'username' : sess['username'], 'bookmarks' : bookmarks, 'tags' : tags}
            self.response.out.write(_renderTemplate('home.html', template_values))

    def post(self):
        sess = gmemsess.Session(self)
        if sess.is_new():
            template_values = {'errors' : ['invalid_session'], 'fields' : {} }
            self.response.out.write(_renderTemplate('landing.html', template_values))
        else:        
            errors = []
            fields = {
                'bmarktitle' : self.request.get('bmarktitle').strip(),
                'bmarklink' : self.request.get('bmarklink').strip(),
                'bmarktags' : self.request.get('bmarktags').strip()
            }
            if self.request.get('bmarktitle').strip() == '':
                errors.append('blank_bmarktitle')
            if self.request.get('bmarklink').strip() == '':
                errors.append('blank_bmarklink')
            if len(errors) == 0:
                usr = _getUserByName(sess['username'])                
                if usr:
                    bmk = Bookmark(title = self.request.get('bmarktitle').strip(),
                        link = self.request.get('bmarklink').strip(),
                        user = usr                    
                    )
                    bmk.put()
                else:
                    errors.append('user_not_found')
            if len(errors) == 0:
                if self.request.get('bmarktags').strip() != '':
                    nams = self.request.get('bmarktags').strip().split(',')
                    for nam in nams:
                        objtag = Tag(name = nam,
                            user = usr                    
                        )
                        objtag.put()
                        bmktag = BookmarkTag(
                            bookmark = bmk,
                            tag = objtag
                        )
                        bmktag.put()
            template_values = {'errors' : errors, 'fields' : fields}
            self.response.out.write(_renderTemplate('home.html', template_values))
        
class LogOutCmd(webapp.RequestHandler):

    def get(self):
        sess = gmemsess.Session(self)
        sess.invalidate()
        self.redirect('/landing')

class PwdRecoverPage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        self.response.out.write(_renderTemplate('pwdrecover.html', template_values))

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

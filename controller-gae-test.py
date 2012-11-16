#!/usr/bin/env python
#
import os
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from model.Categoria import Categoria
from model.Coisa import Coisa

class ControllerInicial(webapp.RequestHandler):
    def get(self):
        template_values = {
            'texto': 'P&aacute;gina Inicial',
            }
        path = os.path.join(os.path.dirname(__file__), 'view/inicial.html')
        self.response.out.write(template.render(path, template_values))        

class ControllerCategoria(webapp.RequestHandler):
    def get(self, pCmd = '', pKey = ''):
        template_values = {}    
        if pCmd == 'listar' or pCmd == '':
            objs = Categoria.all()
            objs.order('descricao')
            template_values = {'objs': objs, 'qtd' : objs.count()}    
            path = os.path.join(os.path.dirname(__file__), 'view/categorias.html')
            self.response.out.write(template.render(path, template_values))        
        elif pCmd == 'novo':
            obj = Categoria(descricao = '')
            template_values = {'obj' : obj, 'key' : ''}    
            path = os.path.join(os.path.dirname(__file__), 'view/categoria.html')
            self.response.out.write(template.render(path, template_values))            
        elif pCmd == 'editar':
            obj = db.get(db.Key(pKey))
            template_values = {'key' : obj.key(), 'descricao' : obj.descricao}
            path = os.path.join(os.path.dirname(__file__), 'view/categoria.html')
            self.response.out.write(template.render(path, template_values))              
        elif pCmd == 'excluir':
            obj = db.get(db.Key(pKey))
            obj.delete()
            self.redirect('/categoria/listar')               
    def post(self, pCmd = ''):
        template_values = {}    
        if pCmd == 'salvar':            
            if self.request.get('key') == '':
                obj = Categoria(descricao = self.request.get('descricao'))
                obj.put()            
            else:
                obj = db.get(db.Key(self.request.get('key')))
                obj.descricao = self.request.get('descricao')   
                obj.put() #db.put(obj)
            self.redirect('/categoria/listar')

class ControllerCoisa(webapp.RequestHandler):
    def get(self, pCmd = '', pKey = ''):
        template_values = {}    
        if pCmd == 'listar' or pCmd == '':
            objs = Coisa.all()
            objs.order('nome')
            template_values = {'objs': objs}    
            path = os.path.join(os.path.dirname(__file__), 'view/coisas.html')
            self.response.out.write(template.render(path, template_values))  
        elif pCmd == 'novo':
            cats = Categoria.all().order('descricao')
            template_values = {'cats' : cats}    
            path = os.path.join(os.path.dirname(__file__), 'view/coisa.html')
            self.response.out.write(template.render(path, template_values))
        elif pCmd == 'editar':
            obj = db.get(db.Key(pKey))
            cats = Categoria.all().order('descricao')
            template_values = {'key' : obj.key(), 'nome' : obj.nome, 'descricao' : obj.descricao, 
                'preco' : obj.preco, 'categoria' : obj.categoria.key(), 'cats' : cats}
            path = os.path.join(os.path.dirname(__file__), 'view/coisa.html')
            self.response.out.write(template.render(path, template_values))             
    def post(self, pCmd = ''):
        template_values = {}    
        if pCmd == 'salvar':            
            if self.request.get('key') == '':
                obj = Coisa()
                obj.nome = self.request.get('nome')
                obj.descricao = self.request.get('descricao')
                prc = self.request.get('preco').replace(',', '.')
                obj.preco = float(prc)
                obj.categoria = db.Key(self.request.get('categoria'))
                obj.put()            
            else:
                obj = db.get(db.Key(self.request.get('key')))
                obj.nome = self.request.get('nome')
                obj.descricao = self.request.get('descricao')
                prc = self.request.get('preco').replace(',', '.')
                obj.preco = float(prc)              
                obj.categoria = db.Key(self.request.get('categoria'))
                obj.put()
            self.redirect('/coisa/listar')            

def main():
    application = webapp.WSGIApplication([('/', ControllerInicial), 
                                            ('/inicio.*', ControllerInicial),
                                            ('/categoria', ControllerCategoria),
                                            (r'/categoria/(.*)/(.*)', ControllerCategoria),
                                            (r'/categoria/(.*)', ControllerCategoria),
                                            ('/coisa', ControllerCoisa),
                                            (r'/coisa/(.*)/(.*)', ControllerCoisa),
                                            (r'/coisa/(.*)', ControllerCoisa),                                            
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

from google.appengine.ext import db
from Categoria import Categoria

class Coisa(db.Model):
    nome = db.StringProperty()
    descricao = db.StringProperty()
    preco = db.FloatProperty()
    categoria = db.ReferenceProperty(Categoria)

from google.appengine.ext import db

class Categoria(db.Model):
    descricao = db.StringProperty() #required=True)
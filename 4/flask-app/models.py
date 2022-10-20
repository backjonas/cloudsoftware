from db import db

class Actor(db.Document):
  name = db.StringField(required=True)
  count = db.IntField()

class Movie(db.Document):
    title = db.StringField(required=True)
    year = db.IntField()
    genres = db.ListField(db.StringField())
    actors = db.ListField(db.ReferenceField('Actor'))

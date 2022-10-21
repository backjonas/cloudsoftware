from database.db import db

class Album(db.Document):
  name = db.StringField(required=True, unique=True)
  description = db.StringField()
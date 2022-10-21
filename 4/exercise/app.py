from flask import Flask, request, jsonify
from bson.objectid import ObjectId
import base64
import codecs
import json

from database.db import initialize_db
from database.models import Photo, Album


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
'host':'mongodb://localhost/flask-database-db'
}

db = initialize_db(app)

def str_list_to_objectid(str_list):
  return list(
    map(
      lambda str_item: ObjectId(str_item),
      str_list
    )
  )

def object_list_as_id_list(obj_list):
  return list(
    map(
      lambda obj: str(obj.id),
      obj_list
    )
  )

def object_list_as_name_list(obj_list):
  return list(
    map(
      lambda obj: str(obj.name),
      obj_list
    )
  )


# Album routes
@app.route('/listAlbum', methods=["POST"])
def add_album():
  body = request.get_json()
  album = Album(**body).save()
  return jsonify({
    'message': 'Album succesfully created',
    'id': str(album.id)
  }), 201

@app.route('/listAlbum', methods=["GET"])
def get_all_albums():
  albums = Album.objects()
  return jsonify(albums), 200

@app.route('/listAlbum/<album_id>', methods=["GET"])
def get_album(album_id):
  album = Album.objects.get_or_404(id=album_id)
  return jsonify(album), 200

@app.route('/listAlbum/<album_id>', methods=["PUT"])
def update_album(album_id):
  body = request.get_json()
  album = Album.objects.get_or_404(id=album_id)
  album.update(**body)
  return jsonify({
    'message': 'Album succesfully updated',
    'id': str(album_id)
  }), 200

@app.route('/listAlbum/<album_id>', methods=["DELETE"])
def delete_album(album_id):
  print(album_id)
  album = Album.objects.get_or_404(id=album_id)
  album.delete()
  return jsonify({
    'message': 'Album succesfully deleted',
    'id': str(album_id)
  }), 200


if __name__ == '__main__':
    app.run()
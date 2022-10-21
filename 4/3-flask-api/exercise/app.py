from flask import Flask, jsonify, request, Response
import json
from bson.objectid import ObjectId
import os
import urllib
import base64
import codecs

from database.db import initialize_db
from database.models import Photo, Album


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
'host':'mongodb://mongo/flask-database'
}

db = initialize_db(app)

def str_list_to_objectid(str_list):
  return list(
    map(
      lambda str_item: ObjectId(str_item),
      str_list
    )
  )

def object_list_as_name_list(obj_list):
  return list(
    map(
      lambda obj: str(obj.name),
      obj_list
    )
  )

# Photo routes
@app.route('/listPhoto', methods=["POST"])
def add_photo():
  try:
    default_album = Album.objects.get(name='Default')
  except Exception as e:
    default_album = Album(name='Default').save()

  posted_image = request.files['image_file']
  posted_data = request.form.to_dict()
  keys = posted_data.keys()
  if posted_data and 'albums' not in keys:
    posted_data['albums'] = [default_album.id]

  photo = Photo(**posted_data)
  photo.image_file.replace(posted_image)
  photo.save()
  return {
    'message': 'Photo succesfully created',
    'id': str(photo.id)
  }, 201

@app.route('/listPhoto/<photo_id>', methods=['GET'])
def get_one_photo(photo_id: str):
  photo = Photo.objects.get_or_404(id=photo_id)
  base64_data = codecs.encode(photo.image_file.read(), 'base64')
  image = base64_data.decode('utf-8')

  return {
    'name': photo.name,
    'tags': photo.tags,
    'location': photo.location,
    'albums': photo.albums,
    'file': image
  }, 200

@app.route('/listPhoto/<photo_id>', methods=['PUT'])
def update_photo(photo_id):
  posted_image = request.files['image_file']
  posted_data = request.form.to_dict()
  keys = posted_data.keys()
  if posted_data and keys:
    if "tags" in keys:
      posted_data["tags"] = str_list_to_objectid(posted_data["tags"])
    if "albums" in keys:
      posted_data["albums"] = str_list_to_objectid(posted_data["albums"])
    photo = Photo.objects.get_or_404(id=photo_id)
    photo.update(**posted_data)
    photo.image_file.replace(posted_image)
    photo.save()

  return {
    'message': 'Photo succesfully updated',
    'id': str(photo_id)
  }, 200

@app.route('/listPhoto/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
  photo = Photo.objects.get_or_404(id=photo_id)
  photo.delete()
  return {
    'message': 'Photo succesfully deleted',
    'id': str(photo_id)
  }, 200

@app.route('/listPhotos', methods=['GET'])
def get_photos():
  args = request.args

  albumName = args.get('albumName', 'Default')
  photo_objects = Photo.objects()
  photo_objects = filter(
    lambda photo: albumName in [album.name for album in photo.albums], 
    photo_objects
  )

  tag = args.get('tag', None)
  if tag is not None:
    photo_objects = filter(
      lambda photo: tag in photo.tags,
      photo_objects
    )

  photos = []
  for photo in photo_objects:
    base64_data = codecs.encode(photo.image_file.read(), 'base64')
    image = base64_data.decode('utf-8')
    photos.append({'name': photo.name, 'location': photo.location, 'file': image})

  return jsonify(photos), 200

# Album routes
@app.route('/listAlbum', methods=["POST"])
def add_album():
  body = request.get_json()
  album = Album(**body).save()
  return {
    'message': 'Album succesfully created',
    'id': str(album.id)
  }, 201

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
  return {
    'message': 'Album succesfully updated',
    'id': str(album_id)
  }, 200

@app.route('/listAlbum/<album_id>', methods=["DELETE"])
def delete_album(album_id):
  print(album_id)
  album = Album.objects.get_or_404(id=album_id)
  album.delete()
  return {
    'message': 'Album succesfully deleted',
    'id': str(album_id)
  }, 200

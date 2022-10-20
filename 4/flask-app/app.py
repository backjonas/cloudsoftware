from flask import Flask, request, jsonify
from db import initialize_db
from models import Movie, Actor
from bson.objectid import ObjectId
# from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
'host':'mongodb://localhost/tutorial-db'
}

db = initialize_db(app)

def str_list_to_objectid(str_list):
    return list(
        map(
            lambda str_item: ObjectId(str_item),
            str_list
        )
    )

# Movie routes
@app.route('/movies', methods=["POST"])
def add_movie():
    body = request.get_json()
    movie = Movie(**body).save()
    return jsonify(movie), 201

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects()
    return jsonify(movies), 200

@app.route('/movies/<movie_id>', methods=['GET'])
def get_one_movie(movie_id: str):
    movie = Movie.objects.first_or_404(movie_id)
    return jsonify(movie), 200

@app.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    body = request.get_json()
    keys = body.keys()
    if body and keys:
        if "actors" in keys:
            body["actors"] = str_list_to_objectid(body["actors"])
        Movie.objects.get(id=movie_id).update(**body)
    return {'id': str(movie_id)}, 200

@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.objects.get_or_404(id=movie_id)
    movie.delete()
    return {'id' : str(movie.id)}, 200

# Actor routes
@app.route('/actors', methods=["POST"])
def add_actor():
    body = request.get_json()
    actor = Actor(**body).save()
    return jsonify(actor), 201


if __name__ == '__main__':
    app.run()
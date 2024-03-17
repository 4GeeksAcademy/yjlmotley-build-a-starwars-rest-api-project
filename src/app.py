"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def list_users():
    # Get the list of users in your database (for example, User.query.all())
    users = User.query.all()

    # Serialize each user and their favorites before converting them to JSON
    serialized_users = []
    for user in users:
        serialized_user = user.serialize()
        # If the user has favorites, serialize each favorite
        if user.favorites:
            serialized_favorites = [favorite.serialize() for favorite in user.favorites]
            serialized_user['favorites'] = serialized_favorites
        serialized_users.append(serialized_user)

    # Convert the list of serialized users to JSON using jsonify
    json_response = jsonify(serialized_users)

    # Returns JSON response
    return json_response, 200

@app.route('/people', methods=['GET'])
def list_people():
    people = Character.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        raise APIException("Person not found", status_code=404)
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def list_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def list_user_favorites():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user is None:
        user = User.query.first()
        if user is None:
            raise APIException("User not found", status_code=404)
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized_favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    
    favorite = Favorite(name="planet", user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    
    favorite = Favorite(name="people", user_id=user_id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite people added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        raise APIException("Favorite planet not found", status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet removed successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    user_id = request.args.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if favorite is None:
        raise APIException("Favorite people not found", status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite people removed successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

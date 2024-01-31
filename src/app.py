"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Activity
from datetime import datetime
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

##Endpoint para listar todas las personas o solo una
@app.route('/people', methods=['GET'])
def all_people():

    people = People.query.all()
    response = [person.serialize() for person in people]
    return jsonify(response), 200

@app.route('/people/<int:id>', methods=['GET'])
def one_people(id):

    person = People.query.get_or_404(id)
    response = person.serialize()
    return jsonify(response), 200


##Endpoint para listar todas los planetas o solo uno
@app.route('/planet', methods=['GET'])
def all_planet():

    planets = Planet.query.all()
    response = [planet.serialize() for planet in planets]
    return jsonify(response), 200

@app.route('/planet/<int:id>', methods=['GET'])
def one_planet(id):

    planet = Planet.query.get_or_404(id)
    response = planet.serialize()
    return jsonify(response), 200


##Endpoint para listar todas los usuarios del blog
@app.route('/users', methods=['GET'])
def all_users():

    records = User.query.all()
    return jsonify(records), 200


##Endpoint para listar todos los favoritos del usuario actual
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def favorited(user_id):

    favorites = Activity.query.filter_by(user_id=user_id, favorite=True).all()
    return jsonify(favorites), 200


##Añadir una nueva persona favorita al usuario actual
@app.route('/users/favorites/people/<int:user_id>/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
   
    existing_favorite = Activity.query.filter_by(user_id=user_id, people_id=people_id).first()

    if existing_favorite:
        abort(400, description="People already marked as favorite")

    new_favorite = Activity(
        user_id=user_id,
        people_id=people_id,
        favorite=True,
        updated_at=datetime.utcnow()
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "People marked as favorite successfully"}), 201


##Añadir un nuevo planeta favorito al usuario actual
@app.route('/users/favorites/planets/<int:user_id>/<int:planets_id>', methods=['POST'])
def add_favorite_planet(user_id, planets_id):
   
    existing_favorite = Activity.query.filter_by(user_id=user_id, planets_id=planets_id).first()

    if existing_favorite:
        abort(400, description="Planet already marked as favorite")

    new_favorite = Activity(
        user_id=user_id,
        planets_id=planets_id,
        favorite=True,
        updated_at=datetime.utcnow()
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Planet marked as favorite successfully"}), 201


##Eliminar una persona de los favoritos del usuario actual
@app.route('/users/favorites/people/<int:user_id>/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(user_id, people_id):
    
    existing_favorite = Activity.query.filter_by(user_id=user_id, people_id=people_id, favorite=True).first()

    if not existing_favorite:
        abort(404, description="Favorite not found")

    existing_favorite.favorite = False
    existing_favorite.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


##Eliminar un planeta de los favoreitos del usuario actual
@app.route('/users/favorites/planets/<int:user_id>/<int:planets_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planets_id):
    
    existing_favorite = Activity.query.filter_by(user_id=user_id, planets_id=planets_id, favorite=True).first()

    if not existing_favorite:
        abort(404, description="Favorite not found")

    existing_favorite.favorite = False
    existing_favorite.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

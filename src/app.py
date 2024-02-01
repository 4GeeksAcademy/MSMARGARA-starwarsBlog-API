"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
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

##ENPOINTS:
##Endpoint para listar todas las personas o solo una
@app.route('/people', methods=['GET'])
def all_people():
    records = People.query.all()
    serialized_records = [people.serialize() for people in records]
    return jsonify(serialized_records), 200
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
    serialized_records = [user.serialize_without_favorites() for user in records]
    return jsonify(serialized_records), 200
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        serialized_user = user.serialize_without_favorites()
        return jsonify(serialized_user), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

##Endpoint para listar todas los favoritos de un usuario del blog
@app.route('/user_favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user:
        serialized_favorites = user.serialize(include_fav_people=True, include_fav_planets=True)
        return jsonify(serialized_favorites), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

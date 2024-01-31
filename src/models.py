from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship("Role")
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    profile_pic = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(10), nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f'<User {self.name}>'
    def serialize(self):
        return {
            "id": self.id,
            "role_id": self.role.serialize(),
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "profile_pic": self.profile_pic,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "active": self.active
        }

class Role(db.Model):
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    people = db.relationship("People")
    planets_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    planets = db.relationship("Planet")
    favorite = db.Column(db.Boolean, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Activity {self.id}, Type: {self.activity_type}>'
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id.serialize(),
            "people": self.people_id.serialize(),
            "planet": self.planets.serialize(),
            "favorite": self.favorite,
            "updated_at": self.updated_at.isoformat()  
        }

class People(db.Model):
    __tablename__='people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(10), nullable=False)
    eye_color= db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    hair_color = db.Column(db.String(10), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    mass = db.Column(db.String(10), nullable=False)
    skin_color = db.Column(db.String(10), nullable=False)
    homeworld_id= db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    homeworld = db.relationship("Planet")
    films = db.relationship("PeopleFilms", back_populates = "people")
    species = db.relationship("PeopleSpecies", back_populates = "people")
    starships = db.relationship("PeopleStarships", back_populates ="people")
    vehicles = db.relationship("PeopleVehicles", back_populates="people")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<People {self.name}>'
    def serialize(self):
        films = list(map(lambda f: f.serialize_films_people(), self.films))
        species = list(map(lambda s: s.serialize_species_people(), self.species))
        starships = list(map(lambda st: st.serialize_starships_people(), self.starships))
        vehicles = list(map(lambda v: v.serialize_vehicles_people(), self.vehicles))
       
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld.serialize(),
            "films": films,
            "species": species,
            "starships": starships,
            "vehicles": vehicles,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }

class Film(db.Model):
    __tablename__='film'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    episode_id = db.Column(db.Integer, nullable=False)
    opening_crawl=db.Column(db.String(250), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    producer = db.Column(db.String(100), nullable=False)
    realase_date = db.Column(db.Date, nullable=False)
    species = db.relationship("FilmsSpecies", back_populates="film")
    starships = db.relationship("FilmsStarships", back_populates="film")
    vehicles = db.relationship("FilmsVehicles", back_populates="film")
    characters = db.relationship("PeopleFilms", back_populates="film")
    planets = db.relationship("FilmsPlanets", back_populates="film")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Film {self.title}>'
    def serialize(self):
        species = list(map(lambda s: s.serialize_films_species(), self.species))
        starships = list(map(lambda st: st.serialize_films_starships(), self.starships))
        vehicles = list(map(lambda v: v.serialize_films_vehicles(), self.vehicles))
        characters = list(map(lambda c: c.serialize_films_characters(), self.characters))
        planets = list(map(lambda p: p.serialize_films_planets(), self.planets))
        
        return {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.realase_date,
            "species": species,
            "starships": starships,
            "vehicles": vehicles,
            "characters": characters,
            "planets": planets,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }

class Planet (db.Model):
    __tablename__='planet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(20), nullable=False)
    rotation_period = db.Column(db.String(10), nullable=False)
    orbital_period = db.Column(db.String(10), nullable=False)
    gravity = db.Column(db.String(20), nullable=False)
    population = db.Column(db.String(20), nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    surface_water = db.Column(db.String(10), nullable=False)
    residents = db.relationship("PlanetsPeople", back_populates="planet")
    films = db.relationship("FilmsPlanets", back_populates="planet")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Planet {self.name}>'
    def serialize(self):
        residents = list(map(lambda r: r.serialize_planet_residents(), self.residents))
        films = list(map(lambda f: f.serialize_planet_films(), self.films))
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "residents": residents,
            "films": films,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }

class Specie(db.Model):
    __tablename__='specie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    classification = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(20), nullable=False)
    average_height = db.Column(db.String(10), nullable=False)
    average_lifespan = db.Column(db.String(10), nullable=False)
    eye_colors = db.Column(db.String(100), nullable=False)
    hair_colors = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(15), nullable=False)
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people = db.relationship("PeopleSpecies", back_populates="specie")
    films = db.relationship("FilmsSpecies", back_populates="specie")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Specie {self.name}>'
    def serialize(self):
        people = list(map(lambda p: p.serialize_specie_people(), self.people))
        films = list(map(lambda f: f.serialize_specie_films(), self.films))
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "eye_colors": self.eye_colors,
            "hair_colors": self.hair_colors,
            "skin_color": self.skin_color,
            "language": self.language,
            "homeworld": self.homeworld,
            "people": people,
            "films": films,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }

class Vehicle(db.Model):
    __tablename__='vehicle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    vehicle_class = db.Column(db.String(20), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    length = db.Column(db.String(10), nullable=False)
    cost_in_credits = db.Column(db.String(20), nullable= False)
    crew = db.Column(db.String(10), nullable=False)
    passengers = db.Column(db.String(10), nullable=False)
    max_atmosphering_speed = db.Column(db.String(10), nullable=False)
    cargo_capacity = db.Column(db.String(10), nullable=False)
    consumables = db.Column(db.String(20), nullable=False)
    films = db.relationship("FilmsVehicles", back_populates="vehicle")
    pilots = db.relationship("PeopleVehicles", back_populates="vehicle")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Vehicle {self.name}>'
    def serialize(self):
        films = list(map(lambda f: f.serialize_vehicle_films(), self.films))
        pilots = list(map(lambda p: p.serialize_vehicle_pilots(), self.pilots))
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "films": films,
            "pilots": pilots,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }

class Starship(db.Model):
    __tablename__='starship'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    starship_class = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.String(20), nullable= False)
    length = db.Column(db.String(10), nullable=False)
    crew = db.Column(db.String(10), nullable=False)
    passengers = db.Column(db.String(10), nullable=False)
    max_atmosphering_speed = db.Column(db.String(10), nullable=False)
    hyperdrive_rating = db.Column(db.String(50), nullable=False)
    mglt = db.Column(db.String(20), nullable=False)       
    cargo_capacity = db.Column(db.String(10), nullable=False)
    consumables = db.Column(db.String(20), nullable=False)
    films = db.relationship("FilmsStarships", back_populates="starship")
    pilots = db.relationship("PeopleStarships", back_populates="starship")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Starship {self.name}>'
    def serialize(self):
        films = list(map(lambda f: f.serialize_starship_films(), self.films))
        pilots = list(map(lambda p: p.serialize_starship_pilots(), self.pilots))
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_rating": self.hyperdrive_rating,
            "mglt": self.mglt,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "films": films,
            "pilots": pilots,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }

class PeopleFilms(db.Model):
    __tablename__='people_films'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people = db.relationship("People")
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship("Film")

    def __repr__(self):
        return f'<PeopleFilms {self.id}>'
    def serialize_films_people(self):
        return {
            "films": self.film.serialize()
        }
    def serialize_films_characters(self):
        return{
            "people": self.people.serialize()
        }

class PeopleSpecies(db.Model):
    __tablename__='people_species'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people = db.relationship("People")
    specie_id = db.Column(db.Integer, db.ForeignKey('specie.id'), nullable=False)
    specie = db.relationship("Specie")

    def __repr__(self):
        return f'<PeopleSpecies {self.id}>'
    def serialize_species_people(self):
        return {
            "species": self.specie.serialize()
        }
    def serialize_specie_people(self):
        return{
            "people": self.people.serialize()
        }
    
class PeopleStarships(db.Model):
    __tablename__='people_starships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people = db.relationship("People")
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'), nullable=False)
    starship = db.relationship("Starship")

    def __repr__(self):
        return f'<PeopleStarships {self.id}>'
    def serialize_starships_people(self):
        return {
            "starships": self.starship.serialize()
        }
    def serialize_starship_pilots(self):
        return{
            "people": self.people.serialize()
        }

class PeopleVehicles(db.Model):
    __tablename__='people_vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people = db.relationship("People")
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    vehicle = db.relationship("Vehicle")

    def __repr__(self):
        return f'<PeopleVehicles {self.id}>'
    def serialize_vehicles_people(self):
        return {
            "vehicles": self.vehicle.serialize()
        }
    def serialize_vehicle_pilots(self):
        return{
            "people": self.people.serialize()
        }

class PlanetsPeople(db.Model):
    __tablename__='planet_people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people = db.relationship("People")
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    planet = db.relationship("Planet")

    def __repr__(self):
        return f'<PlanetsPeople {self.id}>'
    def serialize_planet_residents(self):
        return {
            "people": self.people.serialize()
        }
    
class FilmsSpecies(db.Model):
    __tablename__='films_species'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship("Film")
    specie_id = db.Column(db.Integer, db.ForeignKey('specie.id'), nullable=False)
    specie = db.relationship("Specie")

    def __repr__(self):
        return f'<FilmsSpecies {self.id}>'
    def serialize_films_species(self):
        return {
            "species": self.specie.serialize()
        }
    def serialize_specie_films(self):
        return{
            "films": self.film.serialize()
        }
    
class FilmsStarships(db.Model):
    __tablename__='film_starships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship("Film")
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'), nullable=False)
    starship = db.relationship("Starship")
    
    def __repr__(self):
        return f'<FilmsStarships {self.id}>'
    def serialize_films_starships(self):
        return {
            "starships": self.starship.serialize()
        }
    def serialize_starship_films(self):
        return{
            "films": self.film.serialize()
        }

class FilmsVehicles(db.Model):
    __tablename__='film_vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship("Film")
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    vehicle = db.relationship("Vehicle")

    def __repr__(self):
        return f'<FilmsVehicles {self.id}>'
    def serialize_films_vehicles(self):
        return {
            "vehicles": self.vehicle.serialize()
        }
    def serialize_vehicle_films(self):
        return{
            "films": self.film.serialize()
        }

class FilmsPlanets(db.Model):
    __tablename__='film_planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship("Film")
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    planet = db.relationship("Planet")

    def __repr__(self):
        return f'<FilmsPlanets {self.id}>'
    def serialize_films_planets(self):
        return {
            "planets": self.planet.serialize()
        }
    def serialize_planet_films(self):
        return{
            "films": self.film.serialize()
        }


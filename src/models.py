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
    favorites_people = db.relationship("People", secondary="favorite_people", back_populates='user')
    favorites_planets = db.relationship("Planet", secondary="favorite_planet", back_populates='user')
    
    def __repr__(self):
        return f'<User {self.name}>'
    def serialize_without_favorites(self):
        return {
            "id": self.id,
            "role_id": self.role.serialize(),
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "profile_pic": self.profile_pic,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "active": self.active
        }
    def serialize(self, include_fav_people=True, include_fav_planets=True):
        serialized_data = {
            "User": self.name
        }
        if include_fav_people:
            serialized_data["favorites_people"] = [people.name for people in self.favorites_people]
        if include_fav_planets:
            serialized_data["favorites_planets"] = [planet.name for planet in self.favorites_planets]
        return serialized_data

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

class Favorite_people(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id 
        }
    
class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id 
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
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    homeworld = db.relationship("Planet", back_populates="residents")
    films = db.relationship("Film", secondary='people_films', back_populates='characters')
    species = db.relationship("Specie", secondary='people_species', back_populates='people')
    starships = db.relationship("Starship", secondary='people_starships', back_populates='pilots')
    vehicles = db.relationship("Vehicle", secondary='people_vehicles', back_populates='pilots')
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)
    user = db.relationship("User",secondary="favorite_people", back_populates='favorites_people')

    def __repr__(self):
        return f'<People: {self.name}>'
    
    def serialize(self, include_films=True, include_species=True, include_starships=True, include_vehicles=True, include_homeworld=True):
        serialized_data = {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }
        if include_films:
            serialized_data["films"] = [film.title for film in self.films]
        if include_species:
            serialized_data["species"] = [specie.name for specie in self.species]
        if include_starships:
            serialized_data["starships"] = [starship.name for starship in self.starships]
        if include_vehicles:
            serialized_data["vehicles"] = [vehicle.name for vehicle in self.vehicles]
        if include_homeworld:
            serialized_data["homeworld"] = self.homeworld.name if self.homeworld else None
        return serialized_data
    
class Film(db.Model):
    __tablename__='film'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    episode_id = db.Column(db.Integer, nullable=False)
    opening_crawl=db.Column(db.String(250), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    producer = db.Column(db.String(100), nullable=False)
    realase_date = db.Column(db.Date, nullable=False)
    species = db.relationship("Specie", secondary='films_species', back_populates='films')
    starships = db.relationship("Starship", secondary='film_starships', back_populates='films')
    vehicles = db.relationship("Vehicle", secondary='film_vehicles', back_populates='films')
    characters = db.relationship("People", secondary='people_films' , back_populates='films')
    planets = db.relationship("Planet", secondary='film_planets', back_populates='films')
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Film {self.title}>'
    
    def serialize(self, include_people=True, include_species=True, include_starships=True, include_films=True, include_planets=True):
        serialized_data = {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.realase_date.isoformat(),
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }
        if include_people:
            serialized_data["characters"] = [character.name for character in self.characters]
        if include_species:
            serialized_data["species"] = [specie.name for specie in self.species]
        if include_starships:
            serialized_data["starship"] = [starship.name for starship in self.starships]
        if include_films:
            serialized_data["vehicles"] = [vehicle.name for vehicle in self.vehicles]
        if include_planets:
            serialized_data["planets"] = [planet.name for planet in self.planets]
        return serialized_data

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
    species = db.relationship("Specie", back_populates="homeworld")
    residents = db.relationship ("People", secondary='planet_people', back_populates='homeworld')
    films = db.relationship("Film", secondary='film_planets', back_populates="planets")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)
    user = db.relationship("User",secondary="favorite_planet", back_populates='favorites_planets')

    def __repr__(self):
        return f'<Planet {self.name}>'
    def serialize(self, include_films=True, include_residents=True):
        serialized_data= {
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
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }
        if include_films:
            serialized_data["films"] = [film.title for film in self.films]
        if include_residents:
            serialized_data["residents"] = [people.name for people in self.residents]
        return serialized_data

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
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    homeworld = db.relationship("Planet", back_populates="species")
    people = db.relationship("People", secondary='people_species', back_populates="species")
    films = db.relationship("Film", secondary='films_species', back_populates="species")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Specie {self.name}>'
    def serialize(self, include_people=True, include_films=True, include_homeworld=True):
        serialized_data = {
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
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }
        if include_people:
            serialized_data["people"] = [person.name for person in self.people]
        if include_films:
            serialized_data["film"] = [film.title for film in self.films]
        if include_homeworld:
            serialized_data["homeworld"] = self.homeworld.name if self.homeworld else None
        return serialized_data

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
    films = db.relationship("Film", secondary='film_vehicles', back_populates="vehicles")
    pilots = db.relationship("People", secondary='people_vehicles', back_populates="vehicles")
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Vehicle {self.name}>'
    def serialize(self, include_pilots=True, include_films=True):
        serialized_data = {
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
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }
        if include_pilots:
            serialized_data["pilots"] = [people.name for people in self.pilots]
        if include_films:
            serialized_data["films"] = [film.title for film in self.films]
        return serialized_data
    
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
    films = db.relationship("Film", secondary='film_starships', back_populates="starships")
    pilots = db.relationship("People", secondary='people_starships', back_populates='starships')
    url = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(50), nullable = False)
    edited = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Starship {self.name}>'
    def serialize(self, include_pilots=True, include_films=True):
        serialized_data= {
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
            "url": self.url,
            "created": self.created,
            "edited": self.edited
        }
        if include_pilots:
            serialized_data["pilots"] = [people.name for people in self.pilots]
        if include_films:
            serialized_data["films"] = [film.title for film in self.films]
        return serialized_data

class PeopleFilms(db.Model):
    __tablename__ = 'people_films'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "film_id": self.film_id_id 
        }
    
class PeopleSpecies(db.Model):
    __tablename__='people_species'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    specie_id = db.Column(db.Integer, db.ForeignKey('specie.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "specie_id": self.specie_id
        }
     
class PeopleStarships(db.Model):
    __tablename__='people_starships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "starship_id": self.starship_id
        }
    
class PeopleVehicles(db.Model):
    __tablename__='people_vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "vehicle_id": self.vehicle_id
        }
    
class PlanetsPeople(db.Model):
    __tablename__='planet_people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    def serialize(self):
            return {
                "id": self.id,
                "people_id": self.people_id,
                "planet_id": self.planet_id
            }
    
class FilmsSpecies(db.Model):
    __tablename__='films_species'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    specie_id = db.Column(db.Integer, db.ForeignKey('specie.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "film_id": self.film_id_id,
            "specie_id": self.specie_id
        }
        
class FilmsStarships(db.Model):
    __tablename__='film_starships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "film_id": self.film_id_id,
            "starship_id": self.starship_id
        }
    
class FilmsVehicles(db.Model):
    __tablename__='film_vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "film_id": self.film_id,
            "vehicle_id": self.vehicle_id
        }

class FilmsPlanets(db.Model):
    __tablename__='film_planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "film_id": self.film_id_id,
            "planet_id": self.planet_id
        }
    
   


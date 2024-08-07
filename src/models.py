from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_planet = db.Table('favorite_planet',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

favorite_people = db.Table('favorite_people',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

favorite_vehicle = db.Table('favorite_vehicle',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planets = db.relationship('Planet', secondary=favorite_planet, lazy='subquery',
                                       backref=db.backref('favorite_users', lazy=True))
    favorite_people = db.relationship('People', secondary=favorite_people, lazy='subquery',
                                      backref=db.backref('favorite_users', lazy=True))
    favorite_vehicles = db.relationship('Vehicle', secondary=favorite_vehicle, lazy='subquery',
                                        backref=db.backref('favorite_users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_people": [person.serialize() for person in self.favorite_people],
            "favorite_vehicles": [vehicle.serialize() for vehicle in self.favorite_vehicles]
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    orbital_period = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    birth_year = db.Column(db.String(20), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    height = db.Column(db.String(20), nullable=False)
    mass = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    skin_color = db.Column(db.String(20), nullable=False)
    homeworld = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "species": self.species,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    model = db.Column(db.String(80), nullable=False)
    manufacturer = db.Column(db.String(80), nullable=False)
    vehicle_class = db.Column(db.String(80), nullable=False)
    cost = db.Column(db.String(80), nullable=False)
    speed = db.Column(db.String(80), nullable=False)
    length = db.Column(db.String(80), nullable=False)
    cargo_capacity = db.Column(db.String(80), nullable=False)
    crew = db.Column(db.String(80), nullable=False)
    passengers = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "vehicle_class": self.vehicle_class,
            "cost": self.cost,
            "speed": self.speed,
            "length": self.length,
            "cargo_capacity": self.cargo_capacity,
            "crew": self.crew,
            "passengers": self.passengers
        }
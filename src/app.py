import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Vehicle, favorite_planet, favorite_people, favorite_vehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key")

db.init_app(app)
Migrate(app, db)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/token', methods=['POST'])
def generate_token():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password, password):
        raise APIException('Invalid email or password', status_code=401)

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token}), 200

@app.route('/people', methods=['GET', 'POST'])
def get_all_people():
    if request.method == 'GET':
        people = People.query.all()
        people_list = [person.serialize() for person in people]
        return jsonify(people_list), 200
    if request.method == 'POST':
        data = request.get_json()
        new_person = People(
            name=data['name'],
            birth_year=data['birth_year'],
            species=data['species'],
            height=data['height'],
            mass=data['mass'],
            gender=data['gender'],
            hair_color=data['hair_color'],
            skin_color=data['skin_color'],
            homeworld=data['homeworld']
        )
        db.session.add(new_person)
        db.session.commit()
        return jsonify(new_person.serialize()), 201

@app.route('/people/<int:people_id>', methods=['GET', 'PUT', 'DELETE'])
def get_person(people_id):
    if request.method == 'GET':
        person = People.query.get(people_id)
        if person is None:
            raise APIException('Person not found', status_code=404)
        return jsonify(person.serialize()), 200
    if request.method == 'PUT':
        person = People.query.get(people_id)
        if person is None:
            raise APIException('Person not found', status_code=404)
        
        data = request.get_json()
        person.name = data.get('name', person.name)
        person.birth_year = data.get('birth_year', person.birth_year)
        person.species = data.get('species', person.species)
        person.height = data.get('height', person.height)
        person.mass = data.get('mass', person.mass)
        person.gender = data.get('gender', person.gender)
        person.hair_color = data.get('hair_color', person.hair_color)
        person.skin_color = data.get('skin_color', person.skin_color)
        person.homeworld = data.get('homeworld', person.homeworld)
        db.session.commit()
        return jsonify(person.serialize()), 200
    if request.method == 'DELETE':
        person = People.query.get(people_id)
        if person is None:
            raise APIException('Person not found', status_code=404)
        
        db.session.delete(person)
        db.session.commit()
        return '', 204

@app.route('/planets', methods=['GET', 'POST'])
def get_all_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        planet_list = [planet.serialize() for planet in planets]
        return jsonify(planet_list), 200
    if request.method == 'POST':
        data = request.get_json()
        new_planet = Planet(
            name=data['name'],
            climate=data['climate'],
            diameter=data['diameter'],
            gravity=data['gravity'],
            orbital_period=data['orbital_period'],
            population=data['population'],
            rotation_period=data['rotation_period'],
            surface_water=data['surface_water'],
            terrain=data['terrain']
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['GET', 'PUT', 'DELETE'])
def get_planet(planet_id):
    if request.method == 'GET':
        planet = Planet.query.get(planet_id)
        if planet is None:
            raise APIException('Planet not found', status_code=404)
        return jsonify(planet.serialize()), 200
    if request.method == 'PUT':
        planet = Planet.query.get(planet_id)
        if planet is None:
            raise APIException('Planet not found', status_code=404)
        
        data = request.get_json()
        planet.name = data.get('name', planet.name)
        planet.climate = data.get('climate', planet.climate)
        planet.diameter = data.get('diameter', planet.diameter)
        planet.gravity = data.get('gravity', planet.gravity)
        planet.orbital_period = data.get('orbital_period', planet.orbital_period)
        planet.population = data.get('population', planet.population)
        planet.rotation_period = data.get('rotation_period', planet.rotation_period)
        planet.surface_water = data.get('surface_water', planet.surface_water)
        planet.terrain = data.get('terrain', planet.terrain)
        db.session.commit()
        return jsonify(planet.serialize()), 200
    if request.method == 'DELETE':
        planet = Planet.query.get(planet_id)
        if planet is None:
            raise APIException('Planet not found', status_code=404)
        
        db.session.delete(planet)
        db.session.commit()
        return '', 204

@app.route('/vehicles', methods=['GET', 'POST'])
def get_all_vehicles():
    if request.method == 'GET':
        vehicles = Vehicle.query.all()
        vehicle_list = [vehicle.serialize() for vehicle in vehicles]
        return jsonify(vehicle_list), 200
    if request.method == 'POST':
        data = request.get_json()
        new_vehicle = Vehicle(
            name=data['name'],
            model=data['model'],
            manufacturer=data['manufacturer'],
            vehicle_class=data['vehicle_class'],
            cost=data['cost'],
            speed=data['speed'],
            length=data['length'],
            cargo_capacity=data['cargo_capacity'],
            crew=data['crew'],
            passengers=data['passengers']
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify(new_vehicle.serialize()), 201

@app.route('/vehicles/<int:vehicle_id>', methods=['GET', 'PUT', 'DELETE'])
def get_vehicle(vehicle_id):
    if request.method == 'GET':
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle is None:
            raise APIException('Vehicle not found', status_code=404)
        return jsonify(vehicle.serialize()), 200
    if request.method == 'PUT':
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle is None:
            raise APIException('Vehicle not found', status_code=404)
        
        data = request.get_json()
        vehicle.name = data.get('name', vehicle.name)
        vehicle.model = data.get('model', vehicle.model)
        vehicle.manufacturer = data.get('manufacturer', vehicle.manufacturer)
        vehicle.vehicle_class = data.get('vehicle_class', vehicle.vehicle_class)
        vehicle.cost = data.get('cost', vehicle.cost)
        vehicle.speed = data.get('speed', vehicle.speed)
        vehicle.length = data.get('length', vehicle.length)
        vehicle.cargo_capacity = data.get('cargo_capacity', vehicle.cargo_capacity)
        vehicle.crew = data.get('crew', vehicle.crew)
        vehicle.passengers = data.get('passengers', vehicle.passengers)
        db.session.commit()
        return jsonify(vehicle.serialize()), 200
    if request.method == 'DELETE':
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle is None:
            raise APIException('Vehicle not found', status_code=404)
        
        db.session.delete(vehicle)
        db.session.commit()
        return '', 204

@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        users = User.query.all()
        user_list = [user.serialize() for user in users]
        return jsonify(user_list), 200
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user.serialize()), 200
    if request.method == 'PUT':
        user = User.query.get(user_id)
        if user is None:
            raise APIException('User not found', status_code=404)
        
        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify(user.serialize()), 200
    if request.method == 'DELETE':
        user = User.query.get(user_id)
        if user is None:
            raise APIException('User not found', status_code=404)
        
        db.session.delete(user)
        db.session.commit()
        return '', 204

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    
    favorite_planets = [planet.serialize() for planet in user.favorite_planets]
    favorite_people = [person.serialize() for person in user.favorite_people]
    favorite_vehicles = [vehicle.serialize() for vehicle in user.favorite_vehicles]
    favorites = {
        "planets": favorite_planets,
        "people": favorite_people,
        "vehicles": favorite_vehicles
    }
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user is None or planet is None:
        raise APIException('User or Planet not found', status_code=404)
    
    user.favorite_planets.append(planet)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1  
    user = User.query.get(user_id)
    person = People.query.get(people_id)
    if user is None or person is None:
        raise APIException('User or People not found', status_code=404)
    
    user.favorite_people.append(person)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = 1  
    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(vehicle_id)
    if user is None or vehicle is None:
        raise APIException('User or Vehicle not found', status_code=404)
    
    user.favorite_vehicles.append(vehicle)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1 
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user is None or planet is None:
        raise APIException('User or Planet not found', status_code=404)
    
    user.favorite_planets.remove(planet)
    db.session.commit()
    return '', 204

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1  
    user = User.query.get(user_id)
    person = People.query.get(people_id)
    if user is None or person is None:
        raise APIException('User or People not found', status_code=404)
    
    user.favorite_people.remove(person)
    db.session.commit()
    return '', 204

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = 1  
    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(vehicle_id)
    if user is None or vehicle is None:
        raise APIException('User or Vehicle not found', status_code=404)
    
    user.favorite_vehicles.remove(vehicle)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
       
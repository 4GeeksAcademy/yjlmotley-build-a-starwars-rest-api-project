from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": self.favorites
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    planet = db.relationship("Planet", foreign_keys=[planet_id])
    character = db.relationship("Character", foreign_keys=[character_id])

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    homeworld = db.Column(db.String(250))
    character_pic = db.Column(db.String(250))
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'mass': self.mass,
            'hair_color': self.hair_color,
            'skin_color': self.skin_color,
            'eye_color': self.eyes_color,
            'birth_year': self.birth_year,
            'gender': self.gender,
            'homeworld': self.homeworld,
            'character_pic': self.url
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(20))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(20))
    terrain = db.Column(db.String(20))
    surface_water = db.Column(db.String)
    planet_pic = db.Column(db.String(250))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'diameter': self.diameter,
            'rotation_period': self.rotation_period,
            'orbital_period': self.orbital_period,
            'gravity': self.gravity,
            'population': self.population,
            'climate': self.climate,
            'terrain': self.terrain,
            'surface_water': self.surface_water,
            'planet_pic': self.url
        }
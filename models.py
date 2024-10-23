from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# from serializers import SerializerMixin
from sqlalchemy.orm import validates
import enum

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', back_populates='episode', cascade="all, delete-orphan")


    def episode_serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
 
    def single_episode_serialize(self):
        data = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        data["appearances"] = [appearance_item.appearance_serialize() for appearance_item in self.appearances]
        return data
    

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    appearances = db.relationship('Appearance', back_populates='guest', cascade="all, delete-orphan")

    def guest_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id=db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id=db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)

    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError(f"{key} must be between 1 and 5.")
        return value
    
    def appearance_serialize(self):
        data = {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id
        }    
        data["guest"] = self.guest.guest_serialize()
        return data

    def create_appearance_serialize(self):
        data = {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id
        }    
        data["guest"] = self.guest.guest_serialize()
        data["episode"] = self.episode.episode_serialize()
        return data    
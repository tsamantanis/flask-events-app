from flask_login import UserMixin
from app import db

class Event(db.Model):
    """Event model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='events')
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    equipment = db.relationship('Equipment', back_populates='event')

class Equipment(db.Model):
    """Equipment model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    event = db.relationship('Event', back_populates='equipment')

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(120), nullable = False)
    events = db.relationship('Event', back_populates='user')

    def __repr__(self):
        return f"<User: {self.username}>"
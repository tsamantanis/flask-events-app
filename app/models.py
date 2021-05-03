from flask_login import UserMixin
from app import db

class Event(db.Model):
    """Event model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user = db.relationship('User', back_populates='events')
    equipment = db.relationship('Equipment', back_populates='event')
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_by = db.relationship("User")

class Equipment(db.Model):
    """Equipment model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    event = db.relationship('User', back_populates='event')

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(120), nullable = False)
    events = db.relationship('Event', back_populates='user')

    def __repr__(self):
        return f"<User: {self.username}>"
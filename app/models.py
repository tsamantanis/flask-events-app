from flask_login import UserMixin
from datetime import date
from app import db

class Event(db.Model):
    """Event model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    timeslot = db.Column(db.String(11), nullable=False)
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

    def get_events(self, date_input):
        """Returns list of events for specific employee on given date"""
        date_input = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
        timeslot_events = {
            "09:00-11:00": "",
            "11:00-13:00": "",
            "13:00-15:00": "",
            "15:00-17:00": ""
        }
        for event_i in Event.query.filter_by(equipment_id = self.id, date = str(date_input)):
            event = Event(
                title = event_i['title'],
                equipment = event_i['equipment'],
                color = event_i['color'],
                date = event_i['date'],
                timeslot = event_i['timeslot'],
                user = event_i['user']
            )
            event.id = str(event_i['id'])
            timeslot_events[event.timeslot] = event
        return timeslot_events

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(120), nullable = False)
    events = db.relationship('Event', back_populates='user')

    def __repr__(self):
        return f"<User: {self.username}>"
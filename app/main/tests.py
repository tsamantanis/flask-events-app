import os
import unittest

from datetime import date
 
from app import app, db, bcrypt
from app.models import Equipment, Event, User

"""
Run these tests with the command:
python3 -m unittest app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data = dict(
        username = username,
        password = password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username = 'me1', password = password_hash)
    db.session.add(user)
    db.session.commit()

def create_equipment():
    equipment1 = Equipment(
        name="eq1",
        quantity=1
    )
    equipment2 = Equipment(
        name="eq2",
        quantity=1
    )
    db.session.add(equipment1)
    db.session.add(equipment2)
    db.session.commit()

def create_events():
    event1 = Event(
        title="Example1",
        date="2021-05-13",
        timeslot="09:00-11:00",
        color="#14AEFF",
        user=User.query.one(),
        equipment=Equipment.query.all()[0]
    )
    event2 = Event(
        title="Example2",
        date="2021-05-13",
        timeslot="11:00-13:00",
        color="#14AEFF",
        user=User.query.one(),
        equipment=Equipment.query.all()[1]
    )
    db.session.add(event1)
    db.session.add(event2)
    db.session.commit()
    


class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage(self):
        """Test that the login / signup show up on the homepage."""
        create_user()
        login(self.app, 'me1', 'password')
        create_equipment()
        create_events()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Calendar', response_text)
        self.assertIn('Logout', response_text)
        self.assertIn('Example1', response_text)
        self.assertIn('Example2', response_text)
        self.assertIn('eq1', response_text)
        self.assertIn('Quantity: 1', response_text)
        self.assertIn('09:00-11:00', response_text)
        self.assertIn('11:00-13:00', response_text)

        self.assertIn('New equipment', response_text)
        self.assertIn('Next Day', response_text)
        self.assertIn('Previous Day', response_text)
 
    def test_new_equipment_page(self):
        """Test that the new equipment page shows the form."""
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/new_equipment', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('New Equipment', response_text)
        self.assertIn('Name', response_text)
        self.assertIn('Quantity', response_text)
        self.assertIn('Submit', response_text)

        self.assertNotIn('Calendar ', response_text)
        self.assertNotIn('Logout', response_text)
        self.assertNotIn('Login', response_text)
        self.assertNotIn('Sign up', response_text)

    def test_new_event_page(self):
        """Test that the new event page shows the form."""
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/new_event/2/2021-05-13/11:00-13:00', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('New Event', response_text)
        self.assertIn('Title', response_text)
        self.assertIn('Date', response_text)
        self.assertIn('Timeslot', response_text)
        self.assertIn('Color', response_text)
        self.assertIn('Submit', response_text)

        self.assertNotIn('Calendar ', response_text)
        self.assertNotIn('Logout', response_text)
        self.assertNotIn('Login', response_text)
        self.assertNotIn('Sign up', response_text)
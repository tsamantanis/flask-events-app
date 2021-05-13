import os
import unittest

from datetime import date
 
from app import app, db, bcrypt
from app.models import User

"""
Run these tests with the command:
python3 -m unittest app.auth.tests
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

class AuthTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the login / signup show up on the homepage."""
        create_user()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Login', response_text)
        self.assertIn('Sign up', response_text)
        self.assertIn('Calendar', response_text)

        self.assertNotIn('New equipment', response_text)
 
    def test_homepage_logged_in(self):
        """Test that the calendar shows up on the homepage."""
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Logout', response_text)
        self.assertIn('Calendar', response_text)
        self.assertIn('New equipment', response_text)

        self.assertNotIn('Login', response_text)
        self.assertNotIn('Sign up', response_text)
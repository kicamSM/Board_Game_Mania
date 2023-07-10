"""Routes tests."""

# run these tests like:
#
#    python -m unittest test_routes.py

import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from models import db, User, Game, user_game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"


import requests
from app import app 

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



db.drop_all()
db.create_all()

class AppTestCase(TestCase):
    """Test Routes"""
    
    # def test_display_home(self):
    #     with app.test_client() as client:
    #         # response = requests.get("/")
    #         response = client.get(f'http://{app.config["SERVER_NAME"]}{app.url_for("display_home")}', )
    #     assert response.status_code == 200
    #     assert 'background_image' in response.json()


    def test_display_home(self):
        with app.test_client() as client:
            # allows you to amke requests to the application and tests the response 
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Explore', html)
            
            
    def test_register_user(self):
        with app.test_client() as client:
            resp = client.get("/register")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('For the full experience please register for Board Game Mania', html)
            
    def test_login_user(self):
        with app.test_client() as client:
            resp = client.get("/login")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome back.', html)
            
    def test_logout_user(self):
        with app.test_client() as client:
            resp = client.post('/login', data={'username': 'test_user', 'password': 'password'})
            # resp = client.get("/logout")
            self.assertEqual(resp.status_code, 200)
            # 302 is a redirection to the login page
          
            resp = client.get("/logout")
            self.assertEqual(resp.status_code, 302)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post('/users/delete')
            self.assertEqual(resp.status_code, 302)
            
    def test_display_user(self):
        newUser = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", "password")
        newUser.id = 1
        with app.test_client() as client:
            resp = client.get('/users/1')
            
            self.assertEqual(resp.status_code, 200)
            
    def test_failed_display_user(self):
        with app.test_client() as client:
            resp = client.get('/users/3')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 404)
            self.assertIn("Sorry, that page doesn't exist!", html)
    
    
        
               
        
            
    
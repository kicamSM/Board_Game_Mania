"""Routes tests."""

# run these tests like:
#
#    python -m unittest test_routes.py

import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
# from flask import FlaskClient
import werkzeug
# import mock

from models import db, User, Game, user_game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"


import requests
from app import app, g

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
    def setUp(self):
        
        u1 = User.register(first_name="test_first1", last_name="test_last1", email="email1@email.com", password="testing1", username="test_username1")
        uid1 = 1111
        u1.id = uid1

        u2 = User.register(first_name="test_first2", last_name="test_last2", email="email2@email.com", password="testing2", username="test_username2")
        uid2 = 2222
        u2.id = uid2
        
        g1 = Game(id="ABC123") 
        gid1 = 'ABC123'
        g1.id = gid1
        
        db.session.add(g1)
        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)
        g1 = Game.query.get(gid1)
        
        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2
        
        self.g1 = g1

        self.client = app.test_client()
        
    def tearDown(self):

        game = Game.query.filter_by(id="ABC123").first()
        db.session.delete(game)
        # db.session.commit()
        
        User.query.delete()
        Game.query.delete()
        db.session.commit()
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_display_home(self):
        with app.test_client() as client:
            # allows you to amke requests to the application and tests the response 
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            # self.assertEqual(resp.status_code, 200)
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
            
    def test_edit_user(self):
        new_user4 = User.register("testUser4First", "testUser4Last", "JimDoe@email.com", "testUsername4", "password")
        new_user4.id = 4
        with app.test_client() as client:
            resp = client.get('/users/4/edit')
            html = resp.get_data(as_text=True)
             
            self.assertEqual(resp.status_code, 302)
            
    def test_api_users_games(self):
        """Test api_user_games Route"""
        user = User.query.get(1111)
        user.games = [Game.query.get('ABC123')]
        with app.test_client() as client:
            resp = client.get('/api/users/games')
            html = resp.get_data(as_text=True)
            # raise ValueError(html)
            self.assertEqual(resp.status_code, 302)
            self.assertIn('Redirecting', html)
            
    def test_display_search_games(self):
        """Test display_search games Route"""
        client = werkzeug.test.Client(app)
        form_req = {'q': 'catan'}
        resp = client.get('/api/games/search', data=form_req)
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Search Results', html)
            
    def test_api_search_games(self):
        """Test api_searh_games"""
        client = werkzeug.test.Client(app)
        form_req = {'q': 'catan'}
        resp = client.get('/api/games/search', data=form_req)
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Search Results', html)
    
    def test_log_play_for_user(self):
        """Test log_play_for_user Route"""
        user = User.query.get(1111)
        g.user = user
        with app.test_client() as client:
            resp = client.get('/users/ABC123/log_play')
            html = resp.get_data(as_text=True)
            # raise ValueError(html)
            self.assertEqual(resp.status_code, 200)
          
         
    
            
        
    
        
        
            
    

               
        
            
    
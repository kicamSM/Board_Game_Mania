"""Routes tests."""

# run these tests like:
#
#    python -m unittest tests/test_routes.py
#  run all test files python -m unittest discover -s tests

import os
from unittest import TestCase
# from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from flask import url_for
import werkzeug
import werkzeug.test
# import mock

# from flask_testing import fixtures
from models import db, User, Game, user_game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"


import requests
from app import app, g, CURR_USER_KEY, convert_to_dict, convert_list_to_date

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



db.drop_all()
db.create_all()

class AppTestCase(TestCase):
    """Test Routes"""
    
    def setUp(self):
        
        db.create_all()
        
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
        self.gid1 = gid1

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
    
    # def test_log_play_for_user(self):
    #     """Test log_play_for_user Route"""

    #     game_id = 'ABC123'
    #     # game = Game.query.get('ABC123')
    #     # g_data = game
    #     # g_data['games'] = [game]
    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1.id
            
    #         # resp = client.get('/users/ABC123/log_play')
    #     #     resp = self.client.post(
    #     #     url_for('log_play_for_user', game_id=game_id),
    #     #     data={'min_players': 2, 'max_players': 4},
    #     #     follow_redirects=True
    #     # )
     
        
    #         endpoint = '/users/{}/log_play'.format(game_id)
    #         resp = client.post(
    #         endpoint,
    #         data={'min_players': 2, 'max_players': 4},
    #         follow_redirects=True
    #         )
    #         # g_data = resp.json()
    #         g_data = resp
    #         html = resp.get_data(as_text=True)
          
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('Play logged successfully', resp.data)
    
    # cant figure out how to set the game for this g_data so it is not currently workin
       
        
    def test_name_entry(self):
        """Test name_entry Route"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            form_req = {'q': '2'}
            resp = client.get('/log_play/catan/ABC123/name_entry', data=form_req)
            html = resp.get_data(as_text=True)
      
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('test_username1', html)
        
    def test_name_entry_not_logged_in(self):
        """Test name_entry Route Failure"""
        with self.client as client:

            form_req = {'q': '2'}
            resp = client.get('/log_play/catan/ABC123/name_entry', data=form_req)
            html = resp.get_data(as_text=True)
      
        
        self.assertEqual(resp.status_code, 302)
        
    def test_display_results(self):
        """Test display_results Route"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
            resp = client.get('/match/results')
            html = resp.get_data(as_text=True)
            
        self.assertEqual(resp.status_code, 200)
        self.assertIn('test_username1', html)
    
    def test_api_result_games(self):
        """Test api_result_games Route"""

        game_ids = ['ABC123', 'DEF456']
        # session['game_ids'] = game_ids

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
                sess['game_ids'] = game_ids
            resp = client.get('/api/results')

        self.assertEqual(resp.status_code, 200)
        
    def test_convert_to_dict(self):
        """Test convert_to_dict Function"""
        
        data = [
        ['johndoe@example.com', 2, 345, 1, 100],
        ]

        expected_result = {
        'match_id': 2,
        'email': 'johndoe@example.com',
        'score': 100,
        'win': 1,
        }

        actual_result = convert_to_dict(data)

        self.assertEqual(actual_result, expected_result)
        
    def test_convert_list_to_date(self):
        """Test convert_list_to_date Function"""
        date_list = [2023, 7, 11]
        expected_result = "07/11/2023"

        actual_result = convert_list_to_date(date_list)
        
        self.assertEqual(actual_result, expected_result)
            
    # def test_display_matches(self):
    #     """Test display_matches Route"""
    # may come back to this one
    
    def add_game_to_user(self):
        """Test add_game_to_user Route"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
                
        game = Game.query.get(self.g1)
        db.session.add(game)
        user = User.query.get(self.uid1)
        
        user.games.append(game)
        db.session.commit()
        
        self.assertEqual(self.u1.games, game)
        
    def add_game_to_user_fail(self):
        """Test add_game_to_user Route Intgrity Error"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
                
        game = Game.query.get(self.g1)
        db.session.add(game)
        user = User.query.get(self.uid1)
        
        user.games.append(game)
        db.session.commit()
        
        with self.assertRaises(IntegrityError):
            game = Game.query.get(self.g1)
            db.session.add(game)
        
            user.games.append(game)
            db.session.commit()
            
    def test_display_games(self):
        """Test display_games Route"""
        with self.client as client:
            resp = client.get('/games')
            html = resp.get_data(as_text=True)
            
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Popular Games', html)
        
    def test_api_games(self):
        """"Test api_games Route"""
        with self.client as client:
            resp = client.get('/api/games')
            
        self.assertEqual(resp.status_code, 200)
        
    def test_delete_users_game(self):
        """"Test delete_users_game Route"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
                
        game = self.g1
        user = User.query.get(self.uid1)
        user.games.append(game)

        self.assertEqual(len(user.games), 1)
        
        db.session.commit()
            
        resp = client.get(f'/games/{self.gid1}/delete')
        
        self.assertEqual(len(user.games), 0)
        self.assertEqual(resp.status_code, 302)
        
    def test_api_game(self):
        """Test api_game Route"""
        with self.client as client:
            
            resp = client.get(f'/api/games/{self.g1}')
            
        self.assertEqual(resp.status_code, 200)
        
        
    
            
        
        
        
               
        
        
        
                
        
        
    

                  
         
    
            
        
    
        
        
            
    

               
        
            
    
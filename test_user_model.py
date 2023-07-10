"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from models import db, User, Game, user_game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"



from app import app, g, do_login
# from flask import before_request


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Create test client, add sample data."""
        # db.session.flush()
        # db.drop_all()
        # db.create_all()
        
        # u1.games.delete()
        # User.query.delete()
        # Game.query.delete()
        
        
        u1 = User.register(first_name="test_first1", last_name="test_last1", email="email1@email.com", password="testing1", username="test_username1")
        uid1 = 1111
        u1.id = uid1

        u2 = User.register(first_name="test_first2", last_name="test_last2", email="email2@email.com", password="testing2", username="test_username2")
        uid2 = 2222
        u2.id = uid2
        
        g1 = Game(id="ABC123") 
        gid1 = 'ABC123'
        g1.id = gid1
        
        # note this may not work exactly how you would like because you are adding a game but dont have a method....  might not matter. 

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
        # user = self.u1
        # user.games.delete()
        # User.query.delete()
        # Game.query.delete()
        # db.drop_all()
        # db.create_all()
        
        # user = self.u2
        # user.games.delete()
        
        game = Game.query.filter_by(id="ABC123").first()
        db.session.delete(game)
        # db.session.commit()
        
        User.query.delete()
        Game.query.delete()
        db.session.commit()
        res = super().tearDown()
        db.session.rollback()
        return res

    
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            first_name="test_first",
            last_name="test_last",
            email="test@test.com",
            username="testuser",
            password="another_password"
        )

        db.session.add(u)
        db.session.commit()

        users = User.query.all()
        games = Game.query.all()
        
        self.assertEqual(len(users), 3)
        self.assertEqual(len(games), 1)
        
    def test_repr(self):
        """Test repr of class"""
        u = User(
            id='3',
            first_name="jane",
            last_name="doe",
            email="janeDoe100@test.com",
            username="JaneDoe",
            password="HASHED_PASSWORD"
           )
        
        self.assertTrue(len(repr(u)) > 0)
        self.assertTrue(u.username in repr(u))  
    
    def test_register_pass(self):
        newUser = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", "password")
        db.session.add(newUser)
        db.session.commit()
        
        self.assertEqual(len(User.query.all()), 3)
        
        
    # def test_register_fail(self):
    #     # newUser1 = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", "password")
    #     # db.session.add(newUser1)
    #     # db.session.commit()
    #     # newUser = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", "password")
    #     with self.assertRaises(IntegrityError):
    #         # newUser = User.register("new_user_test_first", "new_user_test_last", "again@email.com", "testUsername3", "testing1")
    #         # new_user = User.register("test_first1", "test_last1", "email1@email.com", "test_username1", "testing1"  )
    #         new_user = User(first_name="test_first1", last_name="test_last1", email="email1@email.com", password="testing1", username="test_username1")
    #         db.session.add(new_user)
    #         db.session.commit()
    # note that this is the one that is not currently working everything else is working
    
    def test_authentication_pass(self): 
        new_user = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", "password")
        
        self.assertTrue(new_user.password.startswith("$2b$"))
    
    def test_authentication_password_fail(self):
        with self.assertRaises(ValueError):
            newUser =  newUser = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", None)
    
    def test_user_game_add(self):
        """Test Can Add a User Game"""
        
        user = self.u2
        game = self.g1
        # user_game_relationship = user_game(user_id=user.id, game_id=game.id)
        # db.session.add(user)
        # db.session.add(game)
        # db.session.add(user_game_relationship)
        user.games.append(game)
        # this is what is putting out the error
        db.session.commit()
        
        self.assertEqual(len(user.games), 1)
        self.assertEqual(user.games[0].id, "ABC123")

# ************TEST USER ROUTES**************************************************

# class UserRoutesTestCase(TestCase):
#     """Test User Routes"""
    # @before_request
    def test_add_user_to_g(self):
        user = self.u1
        
        def set_g_user(user):
            g.user = user
        
        app.before_request(set_g_user(user))
        self.assertEqual(g.user, user)
        
        
    # def test_edit_user(self):
    #     with app.test_client() as client:
    #         resp = client.get(f'/users/{self.uid1}/edit')
    #         html = resp.get_data(as_text=True)
             
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Edit Your Profile.", html)
    
        
    
# *************************************************************************************************
  
    # def test_authorized_game_page_access(self):
    #     """test the authorized game page accessibility"""
    #         # self.setup_followers()

    #       # will need to figure out how to check the g.user so we can checka and see if this is working 
    #     u1 = User.query.get(self.u1.id)
    #     new_game = Game.query.get(self.g1.id)
    #     u1.games.append(new_game)
    #     db.session.commit()
    #     with self.client as c:

    #         resp = c.get(f"/users/{self.g1.id}/add", follow_redirects=True)
            
    #     self.assertEqual(resp.status_code, 200)
    #     # will have to double check this response code 
    #     self.assertEqual(len(self.user_games), 1)
    #     # this may not be correct either.... 
        
    #     # self.assertNotIn("@testuser2", str(resp.data))
    

    # def test_unauthorized_game_page_access(self):
    #     """test the unauthorized game page accessibility"""

    #     new_game = Game.query.get(self.g1.id)
    #     # this one we want there to be a game but no logged in user so global user willbe empty and then you can take that and try and redirect to the add page and should give you an unauthorized message. 

    #     with self.client as c:

    #         resp = c.get(f"/users/{self.g1.id}/add", follow_redirects=True)    
    #     self.assertIn("Access unauthorized", str(resp.data))    
    #     self.assertEqual(resp.status_code, 200)  


    # def test_user_games(self):
    #     # need to add games to test the length of games 
    #     # self.u1.following.append(self.u2)
        
    #     db.session.commit()

    #     self.assertEqual(len(self.u2.following), 0)
    #     self.assertEqual(len(self.u2.followers), 1)
    #     self.assertEqual(len(self.u1.followers), 0)
    #     self.assertEqual(len(self.u1.following), 1)

    #     self.assertEqual(self.u2.followers[0].id, self.u1.id)
    #     self.assertEqual(self.u1.following[0].id, self.u2.id)
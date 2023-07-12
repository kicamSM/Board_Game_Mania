"""User model tests."""

# run these tests like:
#
#    python -m unittest tests/test_user_model.py

import os
from unittest import TestCase

from models import db, User, Game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"

from app import app, g, CURR_USER_KEY

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Create test client, add sample data."""
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

        self.client = app.test_client()
        
    def tearDown(self):
        
        game = Game.query.filter_by(id="ABC123").first()
        db.session.delete(game)
        
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
        """Test Register Function"""
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
        """Test Authentication Pass"""
        new_user = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", "password")
        
        self.assertTrue(new_user.password.startswith("$2b$"))
    
    def test_authentication_password_fail(self):
        """Test Authentication Password Fail"""
        with self.assertRaises(ValueError):
            newUser =  newUser = User.register("testUser3First", "testUser3Last", "JimDoe@email.com", "testUsername3", None)
    
    def test_user_game_add(self):
        """Test Can Add a User Game"""
        
        user = self.u2
        game = self.g1
        
        user.games.append(game)
        db.session.commit()
        
        self.assertEqual(len(user.games), 1)
        self.assertEqual(user.games[0].id, "ABC123")

# ************TEST USER ROUTES**************************************************

# class UserRoutesTestCase(TestCase):
#     """Test User Routes"""
    # @before_request
    # def test_add_user_to_g(self):
    #     user = self.u1
        
    #     # def set_g_user(user):
    #     #     g.user = user
        
    #     # app.before_request(set_g_user(user))
    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1.id
                
    #         print('***********************************')
    #         print(g.user)
    #         print('***********************************')
    #     self.assertEqual(g.user, user)
    # this is not currently working when running with all tests
        
        
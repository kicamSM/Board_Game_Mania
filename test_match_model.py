"""Match model tests."""

# run these tests like:
#
#    python -m unittest test_match_model.py

import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from models import db, User, Game, Match, match_player

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"


from app import app 


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test Match Model"""
    
    def setUp(self):
        db.create_all()
        
        u1 = User.register(first_name="test_firstUSER1", last_name="test_lastUSER1", email="email1@email.comUSER1", password="testingUSER1", username="test_usernameUSER1")
        uid1 = 5555
        u1.id = uid1
        
        u1 = User.query.get(uid1)
        self.u1 = u1
        self.uid1 = uid1
        
        g1 = Game(id="QRS789") 
        gid1 = 'QRS789'
        g1.id = gid1
        
        db.session.add(g1)
        db.session.commit()
        
        g1 = Game.query.get(gid1)
        self.g1 = g1
        self.gid1 = gid1


    def tearDown(self):
        user = User.query.get(5555)
        match = Match.query.filter_by(user_id=user.id).first()
        db.session.delete(match)
       
        User.query.delete()
        Game.query.delete()
        db.session.commit()
        db.drop_all()

    def test_create_match(self):
        """Test Create Match"""
        user = self.u1
        match = Match(game_id=self.gid1, user_id=user.id, win=True)
        db.session.add(match)
        db.session.commit()

        match_from_db = Match.query.filter_by(id=match.id).first()
        self.assertEqual(match.id, match_from_db.id)
        self.assertEqual(match.game_id, match_from_db.game_id)
        self.assertEqual(match.user_id, match_from_db.user_id)
        self.assertEqual(match.win, match_from_db.win)

    def test_serialize_match(self):
        """Test Serialize Match"""
        user = self.u1

        match = Match(game_id=self.gid1, user_id=user.id, win=True)
        db.session.add(match)
        db.session.commit()

        match_data = match.serialize()
        self.assertEqual(match_data["id"], match.id)
        self.assertEqual(match_data["game_id"], match.game_id)
        self.assertEqual(match_data["user_id"], match.user_id)
        self.assertEqual(match_data["win"], match.win)
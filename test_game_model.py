"""User model tests."""

# run these tests like:
#
#    python -m unittest test_game_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from models import db, User, Game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"

from app import app 

db.create_all()

class GameModelTestCase(TestCase):
    """Test views for messages."""
    
    def setUp(self):
        """Create test client, removes amy added data."""
        
        Game.query.delete()
    
    def test_create_game(self):
        
        g1 = Game(id="ABC123")
        db.session.add(g1)
        db.session.commit()

        g2 = Game(id="DEF456")
        db.session.add(g2)
        db.session.commit()

        games = Game.query.all()
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].id, "ABC123")
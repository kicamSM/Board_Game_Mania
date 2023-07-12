"""User model tests."""

# run these tests like:
#
#    python -m unittest tests/test_game_model.py


import os
from unittest import TestCase

from models import db, Game

os.environ['DATABASE_URL'] = "postgresql:///board_game-test"
os.environ['SECRET_KEY'] = "SECRET_KEY"

from app import app 

db.drop_all()
db.create_all()

class GameModelTestCase(TestCase):
    """Test Add Games to Games Table"""
    
    def setUp(self):
        """Create test client, removes any added data."""
        
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
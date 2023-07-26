"""Models for Board Game Mania"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from datetime import datetime
# added this

Base = declarative_base()

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app): 
    """Connect to database."""
    
    db.app = app
    db.init_app(app)
    
      
class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.Text, nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    matches = relationship('Match', backref='user')
    
    games = relationship('Game', secondary='user_game', back_populates='users')
    
      
    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.email} {self.password} {self.username}>"
    
    @classmethod 
    def register(cls, first_name, last_name, email, username, password):
        """Registers user."""
        hashed_pswd = bcrypt.generate_password_hash(password).decode('UTF-8') 
            
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_pswd
        )

        db.session.add(user)
        return user
    
    @classmethod 
    def authenticate(cls, username, password):
        
        user = cls.query.filter_by(username=username).first()

        if user:
            is_authorized = bcrypt.check_password_hash(user.password, password)
            if is_authorized:
                return user

        return False
    
class Game(db.Model):
    """Game Model"""
    __tablename__ = 'games'
    
    id = db.Column(db.String, primary_key=True)
    
    users = relationship('User', secondary='user_game', back_populates='games' )
    
    def __repr__(self):
        return f"<Game {self.id}>"

user_game = db.Table('user_game', 
    # Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('game_id', db.String, db.ForeignKey(Game.id), primary_key=True)
)


    
class Match(db.Model):
    """Matches Model"""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.String, db.ForeignKey('games.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # num_players = db.Column(db.Integer, nullable=False)
    win = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    
    players = relationship('Player', secondary='match_player', back_populates='matches')
    
    def serialize(self): 
        return {
            'id': self.id, 
            'game_id': self.game_id,
            'user_id': self.user_id,
            'win': self.win,
            # 'timestamp': self.timestamp
        }
        
    def __repr__(self):
        return f"<Match {self.id} {self.game_id} {self.user_id}>"
     
    
class Player(db.Model):
    """Players Model"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    matches = relationship('Match', secondary='match_player', back_populates='players' )
    
    def __str__(self):
        return f"<Player {self.id} {self.email}>"
    
    def __repr__(self):
        return f"<Player {self.id} {self.email}>"
    
    
match_player = db.Table('match_player', db.Model.metadata,
    # Base.metadata,
    db.Column('match_id', db.Integer, db.ForeignKey(Match.id), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey(Player.id), primary_key=True),
    db.Column('win', db.Boolean, nullable=False), 
    db.Column('score', db.Integer, nullable=False)
    
)

# class FuaxIntegrityError:
#     pass
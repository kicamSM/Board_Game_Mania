"""Models for Board Game Mania"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa
# added this



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
 
    # usersgames = db.relationship('UserGame', backref=('users'))
        
    users_games = db.relationship('Game', secondary='user_game', backref='users')
    # users_games = db.relationship('Games', secondary='user_game', backref='users')
    
      
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
    
    def __repr__(self):
        return f"<Game {self.id}>"
    
    @classmethod
    def users_games(cls, sess_user_id): 
        """Filters the Users Games from Game table"""
        
        game_objects = cls.query.filter(User.id==sess_user_id).all()
        
        raise ValueError(game_objects) 
        
        return game_objects 
    
    
user_game = db.Table('user_game', 
    # Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('game_id', db.String, db.ForeignKey(Game.id), primary_key=True)
)


# this worked but is not auto populating so the first solution may have been more correct. Try that one. 
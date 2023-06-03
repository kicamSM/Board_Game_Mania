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
    
    games = relationship('Game', secondary='user_game', back_populates='users')
 
    # usersgames = db.relationship('UserGame', backref=('users'))
        
    # users_games = db.relationship('Game', secondary='user_game', backref='users')
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
    
    users = relationship('User', secondary='user_game', back_populates='games' )
    
    def __repr__(self):
        return f"<Game {self.id}>"
    
    # @classmethod
    # def users_games(cls, sess_user_id): 
    #     """Filters the Users Games from Game table"""
        
    #     game_objects = cls.query.filter(User.id==sess_user_id).all()
        
    #     raise ValueError(game_objects) 
        
    #     return game_objects 
    
    
user_game = db.Table('user_game', 
    # Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('game_id', db.String, db.ForeignKey(Game.id), primary_key=True)
)

    
 

    
    
# *************************************************

# user_game = db.Table('user_game', 
#    db.Column('user_id', db.Integer, db.ForeignKey('User.user.id')),
#    db.Column('game_id', db.String, db.ForeignKey('Game.game.id'))
# )

#****************************************************************
    

# user games and class method

# class UserGame(db.Model): 
#     """Users Games Model"""
#     __tablename__ = 'user_game'
    
#     game_id = db.Column(db.String, db.ForeignKey('games.id'), primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
#     def __repr__(self):
#         return f"<UserGame {self.id} {self.game_id} {self.user_id}>"
    
#     @classmethod
#     def users_games(cls, sess_user_id): 
#         """Filters the Users Games from Game table"""
        
#         game_objects = cls.query.filter(UserGame.user_id==sess_user_id).all()
        
#         raise ValueError(game_objects) 
        
#         return game_objects 

# **************************************************
    
class Player(db.Model):
    """Players Model"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
 
    
      
    def __repr__(self):
        return f"<Player {self.id} {self.first_name} {self.last_name} {self.user_id} {self.match_player_id} >"
    
    
    
class Match(db.Model):
    """Matches Model"""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.String, db.ForeignKey('games.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
      
    def __repr__(self):
        return f"<Match {self.id} {self.game_id} {self.user_id}>"
     
# class GameGenre(db.Model):
#     """Games Genres Model"""
#     __tablename__ = 'games_genres'
    
#     game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True)
#     genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)
    
      
#     def __repr__(self):
#         return f"<Department {self.dept_code} {self.dept_name} {self.phone}>"

# class GameLanguage(db.Model):
#     """Games Languages Model"""
#     __tablename__ = 'games_languages'
    
#     game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True)
#     language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), primary_key=True)
    
      
#     def __repr__(self):
#         return f"<GameLanguage {self.game_id} {self.language_id}>"
    
class MatchPLayer(db.Model):
    """Match Player Model"""
    __tablename__ = 'matches_players'
    
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), primary_key=True)
    win = db.Column(db.Boolean, nullable=False)
    
      
    def __repr__(self):
        return f"<MatchPlayer {self.player_id} {self.match_id} {self.win}>"
    
   # **********************************************************
    # Game Table Notes 
        
        # usersgames = db.relationship('UserGame', backref=('game'))
    # def to_dict(self):
    #     # data = {
    #     #     'id': self.id
    #     # }
    #     # return data
        
    #     return {c.id: getattr(self, c.id) for c in self.__table__.columns}
        
    # user = db.relationship('User')
 

    
    
    # **********************************************************
    #alternate tables that I dont think I need anymore..... 
    
    # class Creator(db.Model):
#     """Creators Model"""
#     __tablename__ = 'creators'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name= db.Column(db.String)
    
      
#     def __repr__(self):
#         return f"<Department {self.id} {self.name}>"
    
# class Genre(db.Model):
#     """Genres Model"""
#     __tablename__ = 'genres'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     genre= db.Column(db.String)
    
#     def __repr__(self):
#         return f"<Genre {self.id} {self.genre}>"
    
# class Publisher(db.Model):
#     """Publisher Model"""
#     __tablename__ = 'publishers'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String)
    
      
#     def __repr__(self):
#         return f"<Publisher {self.id} {self.genre}>"
    
# class Language(db.Model):
#     """Languages Model"""
#     __tablename__ = 'languages'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     language = db.Column(db.String)
    
      
    # def __repr__(self):
    #     return f"<Language {self.id} {self.language}>"
    
    
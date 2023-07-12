"""Board Game Mania"""

import warnings
from flask import Flask, render_template, request, jsonify, flash, session, redirect, g

from models import db, connect_db, User, Game, Match, Player, match_player
from flask_session import Session
import datetime
import requests
import json
from forms import RegistrationForm, LoginForm, UserEditForm 
from sqlalchemy.exc import IntegrityError

from sqlalchemy import create_engine
import os

engine = create_engine("postgresql:///board_game_db")


from sqlalchemy.orm import sessionmaker
SQLSessionMaker = sessionmaker(bind = engine)

API_BASE_URL = 'https://api.boardgameatlas.com/api/'
# response = requests.get('https://api.boardgameatlas.com/api/game/prices?game_id=6FmFeux5xH&client_id=yApNU591Nc')


client_id = os.getenv('client_id')
# note you have to use an f string to add this into the response
# response = requests.get(f'https://api.boardgameatlas.com/api/lists?username=trentellingsen&client_id={client_id}')

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///board_game_db'

app.config['SQLALCHEMY_ECHO'] = True

# app.config['SECRET_KEY'] = "iloverollerderby12"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.app_context().push()

try:
    from flask_debugtoolbar import DebugToolbarExtension
    debug = DebugToolbarExtension(app)
except ImportError:
    warnings.warn('Debugging disabled. Install flask_debugtoolbar to enable')
    pass

# db.init_app(app)
# this was not letting the flask app run 
# adds the app on the database after the fact
# entered this from the youtube file 

connect_db(app)

@app.before_request
def add_user_to_g():
    """Add User to Global Variable"""
    
    if CURR_USER_KEY in session:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])
        
    else:
        g.user = None
        
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    
def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        
@app.errorhandler(404)
def page_not_found(e):
    """ Handle 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def display_home():
    """Display home page"""
    
    background_resp = requests.get(f'{API_BASE_URL}/game/images?limit=1&client_id={client_id}') 
    # raise ValueError(background_resp)
    background_data = background_resp.json()

    for result in background_data['images']:
        game_images_b = result['medium']

    return render_template('index.html', game_images_b=game_images_b )

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Create a New User"""
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try: 
            user = User.register(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
            )
      
            db.session.commit()
            
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)
      
        do_login(user)
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')
  
    else: 
      
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Display Login Page"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            do_login(user)
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout User"""
    do_logout()
    flash("You have been logged out!", 'success')
    return redirect('/login')


# @app.route('/users/delete', methods=["POST"])
# def delete_user():
#     """Delete user."""
    
#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     do_logout()

#     db.session.delete(g.user)
#     db.session.commit()

#     return redirect("/register")

# Note that you have not yet institued a way to delete a user.May add this in later.

@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def display_user(user_id): 
    """Display User Details"""
    user = User.query.get_or_404(user_id)
    
    return render_template('details.html', user=user) 

@app.route('/users/<int:user_id>/edit', methods=['GET','POST'])
def edit_user(user_id): 
    """Edit User Details"""
    user = User.query.get_or_404(user_id)
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = UserEditForm(obj=user)
    
    g.user = User.authenticate(form.username.data,
                             form.password.data)
    
    if form.validate_on_submit():
       if not g.user:
        flash("You entered the incorrect password.", "danger")
        return redirect("/")
    
       else: 
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        g.user.username = form.username.data
        g.user.email = form.email.data
        
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(f"/users/{g.user.id}")

    return render_template('edit.html', user=user, form=form)

@app.route('/api/users/games', methods=['GET'])
def api_users_games():
    """API Get User's Games"""
    # user = g.user
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(g.user.id)

    list_of_games = user.games
    
    # May want to put something in there that lets the user know that they have no games. If they have not yet added any games. 

    id_list = []
    
    for game in list_of_games: 
        game_dict = game.__dict__
        # game_id = game_dict['id']
        id_list.append(game_dict['id'])
    
    string_ids = ','.join(id_list)

    response = requests.get(f'{API_BASE_URL}/search?ids={string_ids}&client_id={client_id}')

    games = response.json()
  
    return games 

@app.route('/users/games', methods=['GET'])
def display_users_games():
    """Display User's Games"""
    user = g.user
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    return render_template('users_games.html', user=user)


@app.route('/games/search', methods=['GET'])

def display_search_games(): 
    """Search Games"""
    
    data = session['games']
    jsonify(data)

    return render_template('game_search.html')

@app.route('/api/games/search', methods=['GET', 'POST'])
def api_search_games():
    """API Get Searched Games"""
    form_req = dict(request.form)
    name = form_req['q']
    response = requests.get(f'{API_BASE_URL}/search?name={name}&limit=30&client_id={client_id}')
    g_data = response.json()
    
    return render_template('game_search.html', g_data=g_data)
    

@app.route('/users/<game_id>/log_play', methods=['GET','POST'])
def log_play_for_user(game_id): 
    """Logs a play for user """
    
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    response = requests.get(f'{API_BASE_URL}/search?ids={game_id}&client_id={client_id}')
    # this is returning one game 
    
    g_data = response.json()
 
    min_players = g_data['games'][0]['min_players']
    max_players = g_data['games'][0]['max_players']
    name = g_data['games'][0]['name']
    # raise ValueError(max_players)
    
    return render_template("log_play.html", min_players=min_players, max_players=max_players, name=name, game_id=game_id)

@app.route('/log_play/<string:g_name>/<game_id>/name_entry', methods=['GET','POST'])

def name_entry(g_name, game_id):
    """Name Entry for Players"""
    
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    form_req = dict(request.form)
    num_players = form_req['q']
   
    username = g.user.username
    email = g.user.email

    return render_template('name_entry.html', num_players=num_players, g_name=g_name, username=username, email=email, game_id=game_id)

@app.route('/log_play/<string:g_name>/<game_id>/score', methods=['GET','POST'])
def keep_score(g_name, game_id): 
    """Track the Score"""
    
    names_emails_dict = dict(request.form)
    names_dict = dict(list(names_emails_dict.items())[::2])
    emails_dict = dict(list(names_emails_dict.items())[1::2])
    # raise ValueError(emails_dict)
    emails_list = list(emails_dict.values())
    names_list = list(names_dict.values())
    players_ids_list = []
    

    for email in emails_list: 
        new_player = Player(email=email)
        db.session.add(new_player)
        try: 
            db.session.commit()
        except: 
            db.session.rollback()
            print('this player has already been added')
   
    for one_email in emails_list:
        player = Player.query.filter_by(email=f"{one_email}").first()
        player_id = player.id
        players_ids_list.append(player_id)
        
   
    session['players_ids_list'] = players_ids_list 
            
    for name in names_list: 
        if name == '':
            index = (names_list.index(''))
            nemo = names_list[index]
            player_num = (index + 1)
            nemo = (f'Player {player_num}')
            names_list[index] = nemo
            
            if index == 0:
                names_list[0] = g.user.username
                
    names_list_json = json.dumps(names_list)
    # grabbing names out of form

    return render_template('score.html', names_list_json=names_list_json, g_name=g_name, game_id=game_id)


def check_if_greater_than_all(list_scores):
    """Grabs the largest score"""
    list_scores.sort()
    largest_num = list_scores.pop(); 
    
    return largest_num, all(largest_num > score for score in list_scores)
        

def false_if_not_greater_than_all(list_scores):
    """Returns False if not greater than all scores"""
    _list_scores = list_scores.copy()
    greatest, is_greater_than_all = check_if_greater_than_all(_list_scores)
    return map_greatest(list_scores, greatest, is_greater_than_all)

def map_greatest(list_scores, greatest: int, is_greater_than_all):
    """maps greatest score"""
    list_wins = [is_greater_than_all if score == greatest else False for score in list_scores]
    finish_route(list_wins, list_scores)
    
def finish_route(list_wins, list_scores):
    """Adds Scores to new_match_player table"""
    players_ids = session['players_ids_list']
    match_id = session['match_id']
    max_length = (max(len(players_ids), len(list_wins), len(list_scores)))
    
    for i in range(max_length):
        new_match_player = match_player.insert().values(match_id=match_id, player_id=players_ids[i], win=list_wins[i], score=list_scores[i])
        # raise ValueError(new_match_player)
        db.session.execute(new_match_player)
    db.session.commit()
    return redirect('/match/results')
   

@app.route('/log_play/<game_id>/save/<names_list_json>/<scores>', methods=['GET', 'POST'])
def save_results_in_table(game_id, names_list_json, scores): 
    """Saves Results to match_player Table"""
    # Note to self this is literally to save that information so you can retrieve it from the table in the next route.
    
    # raise ValueError(scores)
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    winStr = request.form['win']
   
    win = json.loads(winStr.lower())
    
    
    new_match = Match(game_id=game_id, user_id=g.user.id, win=win)
    db.session.add(new_match)
    db.session.commit()
    match_id = new_match.id
   
    session['match_id'] = match_id
    string_scores = scores.split(',')
  
    list_scores = []


    for string_score in string_scores:
        integer = int(string_score)
        list_scores.append(integer)
    
    false_if_not_greater_than_all(list_scores)

    return redirect('/match/results')

    
@app.route('/match/results', methods=['GET', 'POST'])
def display_results():
    """Display results"""
    # raise ValueError('beginning of /match/results')
    user = User.query.get_or_404(g.user.id)
    
    list_matches = user.matches
    user_matches = [match.serialize() for match in Match.query.filter(Match.user_id == g.user.id)]
    matches_json = json.dumps(user_matches)
    list_game_ids = []
    
    
    for match in list_matches: 
        list_game_ids.append(match.game_id)
    game_ids_no_dup = list(dict.fromkeys(list_game_ids))
    game_ids_no_dup_json = json.dumps(game_ids_no_dup)
    
    session['game_ids'] = game_ids_no_dup
    
    return render_template('match_results.html', user=user, matches_json=matches_json, game_ids_no_dup_json=game_ids_no_dup_json)

    
@app.route('/api/results', methods=['GET'])
def api_result_games():
    """gets the games that have results"""
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    game_ids = session['game_ids']
    string_ids = ','.join(game_ids)
    
    response = requests.get(f'{API_BASE_URL}/search?ids={string_ids}&client_id={client_id}')
    games = response.json()
    
    return games 

def convert_to_dict(data):
  """Converts the given data into a dictionary."""
#   result = collections.defaultdict(list)
  result = {}
  for row in data:
        email = row[0]
        match_id = row[1]
        # player_id = row[2]
        win = row[3]
        score = row[4]
    
        result = {
            'match_id': match_id, 
            'email': email, 
            'score': score,
            'win': win
        }
  return result

def convert_list_to_date(date_list):
  """Converts a list of integers representing the year, month, and day into a string representing the date in the format mm/dd/yyyy."""
  year = date_list[0]
  month = date_list[1]
  day = date_list[2]
  date = datetime.datetime(year, month, day)
  this_date = date.strftime("%m/%d/%Y")

  return this_date

@app.route('/game/results/<game_id>', methods=['GET'])
def display_matches(game_id):
    """Display Matches for each game"""  
    user_id = g.user.id
    matches = Match.query.filter_by(user_id=user_id, game_id=game_id).all()
    match_ids = []
    timestamps = []
    
    for match in matches:
        date_list = []
        match_id = match.id
        # timestamp = match.timestamp.date
        timestamp = match.timestamp
        year = timestamp.year
        month = timestamp.month 
        day = timestamp.day
       
        date_list.append(year)
        date_list.append(month)
        date_list.append(day)
        
        date = convert_list_to_date(date_list)

        match_ids.append(match_id)
        timestamps.append(date)
    
    all_matches_data = []

    sql_session = SQLSessionMaker()

    for match_id in match_ids:

        query = sql_session.query(
            Player.email, 
            match_player
        )
        match_players = query.join(match_player, Player.id == match_player.c.player_id).filter(match_player.c.match_id == match_id).all()
        list_matches = []
        
        for tuple_data in match_players:
            list_matches.append([item for item in tuple_data])
        # raise ValueError(list_matches)

            list_matches_dict = convert_to_dict(list_matches)  
            all_matches_data.append(list_matches_dict)
    
    match_id_list = json.dumps(match_ids)
    match_data_list_json = json.dumps(all_matches_data)
    timestamps_json = json.dumps(timestamps)
    
    return render_template('game_results_details.html', _game_id=game_id, match_id_list=match_id_list, match_data_list_json=match_data_list_json, timestamps_json=timestamps_json)

    

@app.route('/games/<game_id>/add', methods=['GET', 'POST'])
def add_game_to_user(game_id): 
    """Adds Game to User Games"""
    
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    new_game = Game(id=game_id) 
    # raise ValueError(new_game)
    db.session.add(new_game)
    
    user = User.query.get_or_404(g.user.id)
    
    try: 
        user.games.append(new_game)

    except IntegrityError:
        db.session.rollback()
        game = Game.query.get_or_404(game_id)
        user.games.append(game)
        
    db.session.commit()
    
    return redirect('/users/games')

@app.route('/games', methods=['GET'])
def display_game():
    """Display Games"""
    
    return render_template('games.html')
        
@app.route('/api/games', methods=['GET'])
def api_games():
    """API Get Games"""
    response = requests.get(f'{API_BASE_URL}/search?limit=100&client_id={client_id}')
    games = response.json()
    
    return games 

@app.route('/games/<game_id>/delete', methods=['GET', 'POST'])
def delete_users_game(game_id): 
    """Delete's Users Game"""
    user = User.query.get_or_404(g.user.id)
    game = Game.query.get_or_404(game_id)
    # raise ValueError(game)
    user.games.remove(game)
    db.session.commit()
    
    return redirect('/users/games')

@app.route('/games/<game_id>', methods=['GET'])
def display_game_details(game_id): 
    """Display Game Details"""

    return render_template('game_details.html', game_id=game_id)

@app.route('/api/games/<game_id>', methods=['GET'])
def api_game(game_id):  
    """API Get Game"""
    
    response = requests.get(f'{API_BASE_URL}/search?ids={game_id}&client_id={client_id}')

    game = response.json()

    return game


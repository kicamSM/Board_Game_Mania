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
    """404 NOT FOUND page."""

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
    """Create a New User Page"""
    
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
        # raise ValueError(new_user.id)
        # session['user_id'] = new_user.id
        # raise ValueError(session['user_id'])
        do_login(user)
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')
        # return redirect(f"/users/{g.user.id}")
        # return render_template('Hello')
    # raise ValueError(g.user)
    # return redirect(f"/users/{g.user.id}", form=form)
    else: 
        # flash("The form did not validate", 'danger')
        return render_template('register.html', form=form)
# this is the one we are redirecting to for whatever reason g.user.id is not currecntly working so need to troubleshoot that. 


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Displa Login Page"""
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


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/register")

@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def display_user(user_id): 
    user = User.query.get_or_404(user_id)
    # games = user.games 
    
    return render_template('details.html', user=user) 

@app.route('/users/<int:user_id>/edit', methods=['GET','POST'])
def edit_user(user_id): 
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

# @app.route('/games/search', methods=['GET'])
# def display_searched_games():
    
#     response = requests.get(f'{API_BASE_URL}/search?limit=30&client_id={client_id}')
#     games = response.json()

@app.route('/api/users/games', methods=['GET'])
def api_users_games():
    """API get User's Games"""
    # user = g.user
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(g.user.id)
    # raise ValueError(user)

    list_of_games = user.games
    
    # May want to put something in there that lets the user know that they have no games. If they have not yet added any games. 
    
    id_list = []
    
    for game in list_of_games: 
        game_dict = game.__dict__
        # game_id = game_dict['id']
        id_list.append(game_dict['id'])
    
    string_ids = ','.join(id_list)
    # raise ValueError(string_ids)
    response = requests.get(f'{API_BASE_URL}/search?ids={string_ids}&client_id={client_id}')
    # raise ValueError(response)
    games = response.json()
    # raise ValueError(games)
    
    return games 

@app.route('/users/games', methods=['GET'])
def display_users_games():
    """Display User's Games"""
    user = g.user
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    return render_template('users_games.html', user=user)

# *******************************************************************************************
# currently what I am working on 

@app.route('/games/search', methods=['GET', 'POST'])
# this may not need to be a post method/ standby 
def display_search_games(): 
    """Search Games"""
    
    data = session['games']
    jsonify(data)

    
    return render_template('game_search.html')

@app.route('/api/games/search', methods=['GET', 'POST'])
# @app.route('/api/games/search/<string:name>', methods=['GET', 'POST'])
def api_search_games():
    # def api_search_games(name):
    """API Get Searched Games"""
    # print("api/games/search is running in app.py")
    # raise ValueError(session.get('name'))
    # session.get('name')
    # if 'name' in session: 
    #     name = session['name']
    # raise ValueError(name)
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
    
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    form_req = dict(request.form)
    num_players = form_req['q']
    # raise ValueError(num_players)
    username = g.user.username
    email = g.user.email

    return render_template('name_entry.html', num_players=num_players, g_name=g_name, username=username, email=email, game_id=game_id)

@app.route('/log_play/<string:g_name>/<game_id>/score', methods=['GET','POST'])
def keep_score(g_name, game_id): 
    """Track the Score"""
    # raise ValueError(name)
    
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
    # raise ValueError(emails_list)
    for one_email in emails_list:
        player = Player.query.filter_by(email=f"{one_email}").first()
        player_id = player.id
        players_ids_list.append(player_id)
        
    # raise ValueError(players_ids_list)
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
    # return render_template('score.html', names_list=names_list)


# @app.route('/api/<game_id>/log_play', methods=['Get'])
# def api_log_play(game_id):
#     """API gets the game information to log play"""
    
#     response = requests.get(f'{API_BASE_URL}/search?ids={game_id}&client_id={client_id}')
#     raise ValueError(game_id)
#     raise ValueError(response)
#     game = response.json()
    
#       # all_min_players = [min_players['min_players'] for min_players in g_data['games']]
#     # all_max_players = [max_players['max_players'] for max_players in g_data['games']]
    
#     return game
    
# @app.route('/results/score_data', methods=['POST']) 
# def recieve_match_scores(): 
#     score_data = request.data
#     raise ValueError(score_data)

#     return('this is the data')



def check_if_greater_than_all(list_scores):
    """Grabs the largest score"""
    list_scores.sort()
    largest_num = list_scores.pop(); 
    # raise ValueError(largest_num, all(largest_num > score for score in list_scores))
    
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
    # raise ValueError(win)
    
    new_match = Match(game_id=game_id, user_id=g.user.id, win=win)
    db.session.add(new_match)
    db.session.commit()
    match_id = new_match.id
    # raise ValueError(match_id)
    session['match_id'] = match_id
    string_scores = scores.split(',')
    # raise ValueError(list_scores)
    list_scores = []
    # raise ValueError(list_scores)

    for string_score in string_scores:
        integer = int(string_score)
        list_scores.append(integer)
    
    false_if_not_greater_than_all(list_scores)

    return redirect('/match/results')

    


    # # Note THAT PASSING MY SCORES THROUGH THE URL IS NOT IDEAL I WOULD MUCH RATHER USE AXIOS.POST TO DO THIS. HOWVER, I CANT GET THAT TO FUNCTION SO I AM MOVING FORWARD UNTIL I CAN COME BACK TO IT
    # raise ValueError(type(names_list_json))
    # names_list = json.loads(names_list_json)
    # names_list = names_list_json
    # raise ValueError(names_list)
    # num_players = len(names_list)
    # raise ValueError(len(names_list))
    # user = User.query.get_or_404(g.user.id)*******************************************************************************************************************
        # this=one will be closer to the truth in what you are actually using 
        
    # for player_id in players_ids: 
    #     player = Player.query.get(player_id)
    #     # you need a win for match_player and a score 
    #     new_match_player = match_player.insert().values(match_id=match_id, player_id=player_id, win=True, score=4)
    #     db.session.execute(new_match_player)
        # note that this one is running and adding informtaion to my table which is why I am currenty keeping it
        # try: 
        #     db.session.execute(new_match_player)
        #     db.session.commit()
        #     print('the problem is not here')
        # except: 
        #     db.session.rollback()
        #     return redirect('/match/results')
    #     print('this mtach_player has already been added')
        # raise ValueError('this mtach_player has already been added')
    
    # db.session.commit()
    # this one was working 
    # else:
    # raise ValueError('this is the end')
    
    # raise ValueError(players_ids)
    # session['match_id'] = match_id
    # raise ValueError(match_id)
    
    # return redirect('/match/results')

# list_scores = session['list_scores']

# def check_if_greater_than_all(list_scores):
#     # raise ValueError('list_scores in check if greater than  all', list_scores)
#     list_scores.sort()
#     largest_num = list_scores.pop(); 
#     # raise ValueError(largest_num, all(largest_num > score for score in list_scores))
    
#     return largest_num, all(largest_num > score for score in list_scores)
        
# def map_greatest(list_scores, greatest: int, is_greater_than_all):
   
#     list_wins = [is_greater_than_all if score == greatest else False for score in list_scores]
#     # raise ValueError(list_wins)
#     session['list_wins'] = 'list_wins'
#     return redirect('/add/player_match')
#     # return [is_greater_than_all if score == greatest else False for score in list_scores]

# def false_if_not_greater_than_all(list_scores):
#     _list_scores = list_scores.copy()
#     greatest, is_greater_than_all = check_if_greater_than_all(_list_scores)
#     print(map_greatest(list_scores, greatest, is_greater_than_all))
#     return map_greatest(list_scores, greatest, is_greater_than_all)


# @app.route('/add/player_match', methods=['GET', 'POST'])
# def add_result_to_player_match_table():
    
#         list_scores = session['list_scores']
#         list_wins = session['list_list_wins']
#         raise ValueError('list_wins in add_result_to_player_match', list_wins)
    

    
    
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
        # match_data = []
        
        # dates = Match.query.get(match_id)
        # raise ValueError(dates)
        # note need to get dates out and then you can replace the match id with THAT

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
            # match_data.append(list_matches)
            # raise ValueError(list_matches_dict)
            # match_data.update(list_matches_dict)
            # match_data.append(list_matches_dict)
            # all_matches_data.append(match_data)
            all_matches_data.append(list_matches_dict)
    
    # raise ValueError(all_matches_data)
    # raise ValueError(match_data)
    match_id_list = json.dumps(match_ids)
    # match_data_list = match_data.to_dict()
    # match_data_list_json = json.dumps(match_data)
    match_data_list_json = json.dumps(all_matches_data)
    timestamps_json = json.dumps(timestamps)
    # raise ValueError(type(timestamps_json))
    # raise ValueError(match_data)
    
    return render_template('game_results_details.html', _game_id=game_id, match_id_list=match_id_list, match_data_list_json=match_data_list_json, timestamps_json=timestamps_json)

    

@app.route('/games/<game_id>/add', methods=['GET', 'POST'])
def add_game_to_user(game_id): 
    """Adds Game to User Games"""
    # user = g.user
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



# if __name__ == '__main__':
#     app.run(debug=True)
# from the youtube video 02



# ************************************************************************************************************
# NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES NOTES 
# ************************************************************************************************************



# ************************************************************************************************************
# DESIGN NOTES DESIGN NOTES DESIGN NOTES DESIGN NOTES DESIGN NOTES DESIGN NOTES DESIGN NOTES DESIGN NOTES DESIGN NOTES
# ************************************************************************************************************

# After you click on the results you will be show wins losses and total plays.... After that you can click on the inididual game this will then show you the matches that you have played with that game directly. I would like to be able to make it so each of the matches is then able to be clicked on and and it will show the details of that match... I.E. players, scores, and who won. A nice touch would also be a date and time stamp. From there it would be awesome if you could click on a player who you have played and it would take you to the total of that players stats. 




# so this is actually giving us the data that we want to use, I dont think you need what you have in models.py
    
    # ***********************************************************
    # this is in @app.route('/api/games', methods=['GET'])
    
     # raise ValueError(games)
    # games = { 
    # "names": "[game_name['name'] for game_name in g_data['games']]"
    # }
    
    # raise ValueError(games_data)
    
    # games = [response.serialize() for game in games_data]
    # note that this is retrieving the games from the table and we dont have any games in there so you need to figure out how to retrieve the games from the API 
    # return render_template('games.html', games=games)
    
    # THIS IS WHAT WAS DISPLAYING BEFORE 
    # search = request.args.get('q') 
    # # this is search by name
    
    # games = requests.get(f'{API_BASE_URL}/search?name={search}&limit=30&client_id={client_id}')
    
    # g_data = games.json()
    
    # names = [game_name['name'] for game_name in g_data['games']]
    # # this is looping through and grabbing each name in the list 
    # # raise ValueError(games_name)
    # all_min_players = [min_players['min_players'] for min_players in g_data['games']]
    # all_max_players = [max_players['max_players'] for max_players in g_data['games']]
    # images = [image['images']['medium'] for image in g_data['games']]
    # descriptions = [description['description'] for description in g_data['games']]

    # ************************************************************************
    
    # ****************************************************************
    # THIS IS WHAT WAS DISPLAYING BEFORE 
    # return render_template('games.html', images=images, names=names, all_min_players=all_min_players, all_max_players=all_max_players, descriptions=descriptions)

    # *****************************************************************
    # @app.route('/match/results', methods=['GET', 'POST'])
    # *****************************************************************
       # raise ValueError(game_ids_no_dup)
    # need to save this list in session to grab in additional route that will return the games --> then you can grab the name and pic from that game 
    
    # game id, user_id, win/lose 
    # raise ValueError(user.matches)
    
    # what you want to display is the name of the game number of times played win or loss and num of players 
    # could later add in date and other players etc... 
    
    # name of the game 
        # you can get this through the id making an api call 
    
    #num times game is played     
        #num times played will be from that user id how many matches with that game id 
        
    #num times win for a particular game 
        #num wins for that game num times game is played with num wins
        
    #num times loss for a particular game 
        #num losses for that game num times game is played with num wins
    
    # return render_template('match_results.html', user=user)
    # return redirect('/api/results')

# # ************************************************************************************************************
# @app.route('/log_play/<game_id>/save/<names_list_json>/<scores>', methods=['GET', 'POST'])
# ************************************************************************************************************
 # score_data = request.data
    # string_val = score_data.decode('utf-8')
    # raise ValueError('string_val', string_val)
    # raise ValueError('score_data', score_data)
    
    # content_type = request.headers['Content-Type']
    # content_length = request.headers['Content-Length']
    # # content_body = request.body

    # if content_type is None:
    #     print('***********************************************')
    #     print('The Content-Type header is not set.')
    #     print('***********************************************')
    #     # raise ValueError('content type is none')
    # else:
    #     print('***********************************************')
    #     print('The Content-Type header is set to:', content_type)
    #     print('***********************************************')
    #     # raise ValueError('content type is set to something', content_type)
    # # raise ValueError('content length', content_length)
    # # raise ValueError('body', content_body)
    
    # try:
    #     s = score_data.decode('utf-8')
    # except UnicodeDecodeError:
    #     print('The byte data could not be decoded.')
    # else:
    #     print(s)
    
    # arr = bytes(score_data)
    # s = arr.decode('utf-8')
    # score_data = request.get_json()
    # NEED TO GET THE SCORE DATA FROM THE SCORE.JS SO THAT YOU CAN CREATE A NEW MATCH_PLAYER IN TABLE
    # score_data = json.loads(request.data)
    # raise ValueError(s)
    # raise ValueError(arr)
    # raise ValueError(score_data)
    # raise ValueError(type(score_data))


# ************************************************************************************************************
# @app.route('/log_play/<string:g_name>/<game_id>/score', methods=['GET','POST'])
# ************************************************************************************************************
    
    # if 'num_players' in session:
    #     print('num_players is in session')
        # raise ValueError('num_player is in session')
        #this is currently running can I access this in javascript?  
        
    # raise  ValueError(names_list)
    # raise ValueError(len(form_req))
    # raise ValueError(form_req)
    
    # for i in range(1, len(form_req)):
        # player[i] = form_req[f'player{i}_name']
    
        # console.log(player1)
    
    # player2 = form_req['player2_name']
    # raise ValueError(player2)
    # form = ScoreNameForm()
    
    # for key, value in form_req.items():
    #     raise ValueError(key, value)
    
    # for k, v in form_req.items():
    #     if player[0] == v[0]:
    #         print(k, v)
    
    # locals().update(form_req)
    
    # print(player1) 
    
    # for key,val in form_req.items():
    #     exec(key + '=val')
        
    # raise ValueError(form_req)
    
    # if form.validate_on_submit():
    #     first_name = form.first_name.data
    #     last_name = form.last_name.data
    #     user_id = form.user_id.data
    
    # session['names_list'] = names_list
    # session.add(names_list)
    # session.commit()
    
    # session['num'] = 42
    # session.add(names_list)
    # session.commit()

    # raise ValueError(session['names_list'])  


# ************************************************************************************************************
# BEGINNING NOTES 
# ************************************************************************************************************
        # test = requests.get(f'{API_BASE_URL}/search?ids=vJkLBDgn1j&limit=10&client_id={client_id}')
    
  
    # g_data = test.json()
    # print(g_data)
    
    # data = json.loads(response.text)
    # convert data to dict 
    # raise ValueError(data)
    # print(data)

    # data = json.dumps(data)
    #convert data to string 
    # print(data)
    # print(type(data))
    
    # min_players = g_data['games'][0]['min_players']
    # max_players = g_data['games'][0]['max_players']
    # name = g_data['games'][0]['name']
    # description = g_data['games'][0]['name']
    
    # sessionStorage.setItem("data", JSON.stringify(games))
    # session['games'] = games.__dict__
    # print(session['games'])
    
    # session['games'] = data
    
    # new_data = session['games']
    
    # session.commit() this was not working 
    
    # print('data in session', session)
    # when storingvalue in session the data is being emptied ???? Object is there values are not.... 
    
    # localStorage.setItem('games', data)
    # print(localStorage.games)
    
    # return redirect(url_for('display_search_games', games=games))
    # return redirect('/games/search')
    # print(g_data)
    
   
# @app.route('/games/search/var', methods=['GET', 'POST'])
# def get_search_variable():
#     """API Get Searched Games"""
    
#     print("/games/search/var is running in app.py")
#     form_req = dict(request.form)
#     # session['name'] = form_req['q']
#     name = form_req['q']
#     # session['name'] = name
#     # raise ValueError(name)
#     # db.session.add(name)
    
#     return redirect(url_for('api_search_games', name=name))
  
    # could do radio button to click what you are search for. Could also check multiple responses and see if a response returns back something??? 
    # search = request.args.get('q') 
    # raise ValueError(request.values)
    # name = request.args.get('q') 
    # name = request.form.get("id")

    
    # raise ValueError(request.args)
    # name = request.get_data('q')
    # this is returning None 
    # name = request.args.getlist('q')
    
    # if request.method == 'POST': 
    # form_req = dict(request.form)
    # raise ValueError(form_req)
    # name = form_req['q']
    # raise ValueError(name)
    
    # raise ValueError(form_req['q'])
    # raise ValueError(request.form)
    # raise ValueError(dict(request.form.get()))
    # raise ValueError(request.form)
    # raise ValueError('name:', name)
    # get the value in the search bar
    # response = requests.get(f'{API_BASE_URL}/search?name={name}&limit=10&client_id={client_id}')
    # response = requests.get(f'{API_BASE_URL}/search?limit=100&client_id={client_id}')
    # https://api.boardgameatlas.com/api/search?name=Catan&client_id=JLBr5npPhV
    # raise ValueError(response)
        
    # games = response.json()
    # return games 
    
    
    # raise ValueError(games)
    # return redirect(url_for(display_search_games(), games=games))
    
    # return games
    # raise ValueError(games)
    # return render_template('this will be the searched games page')

# *******************************************************************************************

# ************************************************************************************************************
# working on 6/27/2023

# @app.route('/log_play/<game_id>/save/<names_list_json>/<scores>', methods=['GET', 'POST'])
# def save_results_in_table(game_id, names_list_json, scores): 
#     """Saves Results to match_player Table"""
#     # Note to self this is literally to save that information so you can retrieve it from the table in the next route.
    
#     # raise ValueError(scores)
#     if not g.user:
#         flash("Please make an account to use this feature.", "danger")
#         return redirect("/")
    
# # Note THAT PASSING MY SCORES THROUGH THE URL IS NOT IDEAL I WOULD MUCH RATHER USE AXIOS.POST TO DO THIS. HOWVER, I CANT GET THAT TO FUNCTION SO I AM MOVING FORWARD UNTIL I CAN COME BACK TO IT
#     # raise ValueError(type(names_list_json))
#     # names_list = json.loads(names_list_json)
#     names_list = names_list_json
#     # raise ValueError(names_list)
#     num_players = len(names_list)
#     # raise ValueError(len(names_list))
#     user = User.query.get(g.user.id)
#     winStr = request.form['win']
#     win = json.loads(winStr.lower())
#     # raise ValueError(win)
    
#     new_match = Match(game_id=game_id, user_id=g.user.id, win=win, num_players=num_players)
#     # new_match = Match(game_id=game_id, user_id=g.user.id, win=win, num_players=num_players)
#     db.session.add(new_match)
#     db.session.commit()
    
#     match_id = new_match.id
#     # raise ValueError(match_id)
    
#     session['match_id'] = match_id
    
#     # match = Match.query.get(match_id)
#     # raise ValueError(match)
    
#     string_scores = scores.split(',')
#     # raise ValueError(list_scores)
#     list_scores = []
#     # raise ValueError(list_scores)


#     for string_score in string_scores:
#         integer = int(string_score)
#         list_scores.append(integer)
        
#     # raise ValueError(list_scores)
    
#     matches_players = Player.query.join(match_player).join(Match).filter_by(id=match_id).all()
#     raise ValueError(matches_players)
    
#     # if len(list_scores = len())
#     # check_if_greater_than_all(list_scores)
#     false_if_not_greater_than_all(list_scores)

#     # list_wins = []
#     # list wins will look something like [false, false, true, false]
#     # raise ValueError(list_scores)
#     # session['list_scores'] = 'list_scores'
    
# def check_if_greater_than_all(list_scores):
#     # raise ValueError('list_scores in check if greater than  all', list_scores)
#     list_scores.sort()
#     largest_num = list_scores.pop(); 
#     # raise ValueError(largest_num, all(largest_num > score for score in list_scores))
    
#     return largest_num, all(largest_num > score for score in list_scores)
        

# def false_if_not_greater_than_all(list_scores):
#     _list_scores = list_scores.copy()
#     greatest, is_greater_than_all = check_if_greater_than_all(_list_scores)
#     print(map_greatest(list_scores, greatest, is_greater_than_all))
#     return map_greatest(list_scores, greatest, is_greater_than_all)

# def map_greatest(list_scores, greatest: int, is_greater_than_all):
   
#     list_wins = [is_greater_than_all if score == greatest else False for score in list_scores]
#     finish_route(list_wins, list_scores)
    
# def finish_route(list_wins, list_scores):
#     print('*************************************************')
#     print('how many times is this function running????')
#     print('*************************************************')

#     # raise ValueError(list_wins)
#     players_ids = session['players_ids_list']
#     # raise ValueError(players_ids)
#     # raise ValueError(players_ids)
#     # list_scores = session['list_scores']
#     # raise ValueError(list_scores)
#     match_id = session['match_id']
#     # raise ValueError(match_id)
#     # match = Match.query.get(match_id)
#     # raise ValueError(players_ids)
#     # raise ValueError(list_wins)
#     # session['list_wins'] = 'list_wins'
        
#     # maybe could do something like 
#     # for x, y, z in itertools.product(list1, list2, list3):
    
#     max_length = (max(len(players_ids), len(list_wins), len(list_scores)))
    
#     for i in range(max_length):
#     # for player_id, win, score in (players_ids, list_wins, list_scores): 
#         # this is using itertools
#         # player = Player.query.get(players_ids[i])
#         # raise ValueError(player)
#         # you need a win for match_player and a score 
#         new_match_player = match_player.insert().values(match_id=match_id, player_id=players_ids[i], win=list_wins[i], score=list_scores[i])
#         # raise ValueError(new_match_player)

#         # raise ValueError(player)
#         # player.matches.append(match)
#         try:
#             db.session.execute(new_match_player)
#             db.session.commit()
#             return redirect('/match/results')
            
#         except IntegrityError:
#             pass
#             return redirect('/match/results')
#     return redirect('/match/results')
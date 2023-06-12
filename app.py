"""Board Game Mania"""

import warnings
from flask import Flask, render_template, request, jsonify, flash, session, redirect, g, url_for
from models import db, connect_db, User, Game, Player, Match
from flask_session import Session
# note you have to install this as pip3 install flask-session
# UserGame, 
# , Creator, Genre, Publisher, Language
# from board_game_mania import GameClass 
import requests
import json
from forms import RegistrationForm, LoginForm, UserEditForm, ScoreNameForm
from sqlalchemy.exc import IntegrityError

API_BASE_URL = 'https://api.boardgameatlas.com/api/'
# response = requests.get('https://api.boardgameatlas.com/api/game/prices?game_id=6FmFeux5xH&client_id=yApNU591Nc')

client_id = "3Ya324qQb2"
# note you have to use an f string to add this into the response
# response = requests.get(f'https://api.boardgameatlas.com/api/lists?username=trentellingsen&client_id={client_id}')

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///board_game_db'


app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "iloverollerderby12"
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
        g.user = User.query.get(session[CURR_USER_KEY])
        
    else:
        g.user = None
        
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    
def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    

@app.route('/', methods=['GET'])
def display_home():
    
    background_resp = requests.get(f'{API_BASE_URL}/game/images?limit=1&client_id={client_id}') 
    
    background_data = background_resp.json()

    for result in background_data['images']:
        game_images_b = result['medium']
    
    # raise ValueError(game_images)
    
    
    
    return render_template('index.html', game_images_b=game_images_b )

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    
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
            # new_user = User.register(first_name, last_name, email, username, password)
            # raise ValueError(user)
        # raise ValueError(new_user)

        # db.session.add(new_user)
        # try:
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
        flash("The form did not validate", 'danger')
        return render_template('register.html', form=form)
# this is the one we are redirecting to for whatever reason g.user.id is not currecntly working so need to troubleshoot that. 


@app.route('/login', methods=['GET', 'POST'])
def login_user():
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
    
    user = User.query.get(g.user.id)
    
    
    list_of_games = user.games
    # print(list_of_games)
    # raise ValueError(list_of_games)
    # returning empty list currently check the classmethod 
    
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
    
    # this function you need to adjust so that it is the users games and not every users games is the same. 
    # You will need to adjust your schema so that it is not returning all games but it is returning all games associated with that user. Will need an additional table 
    
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
    print('display search games is running in app.py')
    # work on this route tomorrow 
    # will want to return by game name at least and maybe other things like artists etc.... 
    # games=games
    # raise ValueError('games:', games)
    
    # string_data = session['data']
    # string_data = session.get('data')
    # raise ValueError(string_data)
    # if session.get('data') == True:
    #     return 'there is session data'
    # else: 
    #     print('nothing appears to be in session')
    
    # data = session.get('games')
    data = session['games']
    jsonify(data)
    
    print('data from dispaly search games:', data)
    
    
    
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

@app.route('/users/<game_id>/log_play', methods=['GET','POST'])
def log_play_for_user(game_id): 
    """Logs a play for user """
    print('/users/<game_id>/log_play is running in app.py')
    
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    # form = ScoreNameForm()
    # if form.validate_on_submit():
    #     first_name = form.first_name.data
    #     last_name = form.last_name.data
    #     user_id = form.user_id.data
    
    # raise ValueError(game_id)
    
    response = requests.get(f'{API_BASE_URL}/search?ids={game_id}&client_id={client_id}')
    # this is returning one game 
    
    g_data = response.json()
    # raise ValueError(g_data)

    # min_players = [min_players['min_players'] for min_players in g_data['games']]
    # raise ValueError(min_players)
    # max_players = [max_players['max_players'] for max_players in g_data['games']]
    min_players = g_data['games'][0]['min_players']
    max_players = g_data['games'][0]['max_players']
    name = g_data['games'][0]['name']
    # raise ValueError(max_players)
    
    return render_template("log_play.html", min_players=min_players, max_players=max_players, name=name)

@app.route('/log_play/<string:g_name>/name_entry', methods=['GET','POST'])
def name_entry(g_name):
    form_req = dict(request.form)
    num_players = form_req['q']
    username = g.user.username

    # session['num_players'] = num_players

    return render_template('name_entry.html', num_players=num_players, g_name=g_name, username=username)

@app.route('/log_play/<string:name>/score', methods=['GET','POST'])
def keep_score(name): 
    """Track the Score"""
    # raise ValueError(name)
    names_dict = dict(request.form)
    
    # if val in names_dict.value == None: 
    #     val = Player(names_dict.index('val'))
    
    names_list = list(names_dict.values())
    # raise ValueError(names_list)
    # if '' in names_list: 
    for name in names_list: 
        if name == '':
            index = (names_list.index(''))
            nemo = names_list[index]
            player_num = (index + 1)
            nemo = (f'Player {player_num}')
            names_list[index] = nemo

    names_list_json = json.dumps(names_list)
    # grabbing names out of form
    
    
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

    return render_template('score.html', names_list_json=names_list_json)
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
    
    
    
    

@app.route('/games/<game_id>/add', methods=['GET', 'POST'])
def add_game_to_user(game_id): 
    """Adds Game to User Games"""
    # user = g.user
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    new_game = Game(id=game_id) 
    db.session.add(new_game)
    
    user = User.query.get(g.user.id)
    
    try: 
        user.games.append(new_game)

    
    except IntegrityError:
        db.session.rollback()
        game = Game.query.get(game_id)
        user.games.append(game)
        
    db.session.commit()
    
    return redirect('/games')

@app.route('/games', methods=['GET'])
def display_game():
    """Display Games"""
    
    return render_template('games.html')
        
@app.route('/api/games', methods=['GET'])
def api_games():
    """API Get Games"""
    response = requests.get(f'{API_BASE_URL}/search?limit=100&client_id={client_id}')
    games = response.json()
    
    # raise ValueError(games)
    # games = { 
    # "names": "[game_name['name'] for game_name in g_data['games']]"
    # }
    
    # raise ValueError(games_data)
    
    # games = [response.serialize() for game in games_data]
    # note that this is retrieving the games from the table and we dont have any games in there so you need to figure out how to retrieve the games from the API 
    # return render_template('games.html', games=games)
    return games 
# so this is actually giving us the data that we want to use, I dont think you need what you have in models.py
    
    # ***********************************************************
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
    
@app.route('/games/<game_id>/delete', methods=['GET', 'POST'])
def delete_users_game(game_id): 
    """Delete's Users Game"""
    user = User.query.get(g.user.id)
    game = Game.query.get(game_id)
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
# from the youtube video 
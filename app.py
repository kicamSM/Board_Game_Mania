"""Board Game Mania"""

import warnings
from flask import Flask, render_template, request, jsonify, flash, session, redirect, g
from models import db, connect_db, User, Game, Player, Match
# UserGame, 
# , Creator, Genre, Publisher, Language
# from board_game_mania import GameClass 
import requests
from forms import RegistrationForm, LoginForm, UserEditForm
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

@app.route('/games/search', methods=['GET'])
def search_games(): 
    """Search Games"""
    # work on this route tomorrow 
    # will want to return by game name at least and maybe other things like artists etc.... 
    return render_template('searched_games.html')
    
@app.route('/api/games/search', methods=['GET'])
def get_searched_games():
    """Get Searched Games"""
    
    # return games 
    return render_template('this will be the searched games page')

@app.route('/users/<game_id>/log_play', methods=['GET','POST'])
def log_play_for_user(game_id): 
    """Logs a play for user """
    
    if not g.user:
        flash("Please make an account to use this feature.", "danger")
        return redirect("/")
    
    return("this will log a play")
    
    

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

@app.route('/games', methods=['GET'])
def display_game():
    """Display Games"""
    
    return render_template('games.html')

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
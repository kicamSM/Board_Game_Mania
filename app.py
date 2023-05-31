"""Board Game Mania"""

import warnings
from flask import Flask, render_template, request, jsonify, flash, session, redirect, g
import requests
from models import db, connect_db, User, Creator, Genre, Publisher, Language, Game, Player, Match
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
            session['user_id'] = user.id
            return redirect('/tweets')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout User"""
    do_logout()
    flash("You have been logged out!", 'success')
    return redirect('/login')

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

@app.route('/games', methods=['GET'])
def display_game():
    """Display Game"""
    response = requests.get(f'{API_BASE_URL}/search?limit=30&client_id={client_id}')
    
    games = response.json()
    
    # games = { 
    
    # "names": "[game_name['name'] for game_name in g_data['games']]"
    
    # }
    
    # raise ValueError(games_data)
    
    # games = [response.serialize() for game in games_data]
    # note that this is retrieving the games from the table and we dont have any games in there so you need to figure out how to retrieve the games from the API 
    # return render_template('games.html', games=games)
    return jsonify(games)
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
    
    
    # use game object instead of images
    # games = requests.get(f'{API_BASE_URL}/game/images?limit=100&client_id={client_id}')
        
    # games_data = games.json()
    # raise ValueError(games_data)
    
    # raise ValueError(games_data)

    # games_id = [game_id["id"] for game_id in games_data["images"]]
    
    # raise ValueError(games_id)

    # raise ValueError(games_data['images'][1])
    # returns single games_data at index of one

    # for result in games_data['images']:
    #     game_images = result['medium']
    # game_images = [game_image["medium"] for game_image in games_data["images"]]
    
        # return game_images
    # raise ValueError(game_images)
        # raise ValueError(games_data['images'])
        # raise ValueError(result['medium'])
        # raise ValueError(game_images)
        
        # for game_image in game_images:
        #     return game_image
        
        # You can absolutely build a list of dictionaries to do that:
# game_images = [{"img": result["medium"], "id": result["id"]} for result in games_data["images"]]
    
    # if not search: 
    #     games = Game.query.all()
    # else:
           
    # games_data = games.json()
    # raise ValueError(data)
    
    # games_data = g_data['games']
    
  
    
    # game_images = [game_image["medium"] for game_image in games_data["images"]]
    # games_id = [game_id["id"] for game_id in games_data["images"]]
    
    # names = [game_data[0] for game_data in games_data['name']]
    
    # names = game_data[0]['name']
    
  
    # all_min_players = game_data[1]['min_players']
    # all_max_players = game_data[1]['max_players']
    # images = game_data[1]['images']['medium']
    # descriptions = game_data[1]['description']
    # raise ValueError(image)
    
    
    # raise ValueError(game_data[1]['description'])  

    
    # raise ValueError(game_data)
    # so my assumption is that we are going to want t write this in json so that I can use react and pass in lists and access them all etc...
    
    # ****************************************************************
    # THIS IS WHAT WAS DISPLAYING BEFORE 
    # return render_template('games.html', images=images, names=names, all_min_players=all_min_players, all_max_players=all_max_players, descriptions=descriptions)

    # *****************************************************************

Board Game Mania

Introduction 

    "Board Game Mania" is a board game collection application. This application allows users to add their own board games to "My Board  Games list" after an account is created. This application can then be used to log plays of any board games in "My Board Games List". When logging a play, this application will automatically generate a score board based on the number of players the user selects. You can then track the scores of all players and save the match. 

    After saving the match, the user can view all his board games based on total wins, losses, and games played. He can then click on a specific game to view the match details which include  scores for each player, win for each player, date played and emails of players.

    This web application is built with Python and Flask. It uses a free third party API (https://www.boardgameatlas.com/api/docs) that allows any user to search for board games. Board Game Mania uses the PostgreSQL database to store and save information.

    This application is functional and ready to use. However, there are more features that I would like to continue integrating. One of these features is I would like a user to be able to access the total wins and losses of every player in any match they have competed in. I would also like a player to be able to sign up for the application with the email he has used to play. This would then automatically preload any games that he has played into his "games list" as well as all of the match details from his previous played games.

Features 
    -Easy to use
    -Add games to users games 
    -Log plays of games in users games which tracks score
    -Save matches 
    -Access saved matches and details from the match such as scores, whether or not a player won or loss, date of the match, and players emails

Requirements 

    -Python 
    -Flask 
    -SQLAlchemy 
    -PostgreSQL
    -psycopg2
    -Bcrypt

Installation

    -Clone the repository
    -Install the dependencies
    -pip install -r requirements.txt

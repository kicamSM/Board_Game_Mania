"""Utilities related to Board Game Mania"""

class GameClass: 
    def __init__(self, id):
        self.id = id
        
        
        
# import requests

# term = "Madonna"
# response.text
# response = requests.get('https://itunes.apple.com/search', params={'term': term, 'limit':5})

# data = res.json()

# for result in data['results']: 
#     print(result['trackName'])
#     print(result['collectionName'])

# response = requests.get('https://api.boardgameatlas.com/api/search?order_by=rank&ascending=false&client_id= yApNU59lNc')
API_BASE_URL = 'https://api.boardgameatlas.com/api/'
client_id = "3Ya324qQb2"

# response = requests.get('https://api.boardgameatlas.com/api/search?order_by=rank&ascending=false&client_id= yApNU59lNc')

# response = requests.get('https://api.boardgameatlas.com/api/game/prices?game_id=6FmFeux5xH&client_id=JLBr5npPhV')
# note this returns 

# response = requests.get('https://api.boardgameatlas.com/api/game/prices?game_id=6FmFeux5xH&client_id=3Ya324qQb2')

# response = requests.get('https://api.boardgameatlas.com/api/game/images?limit=2&client_id="client_id"')
# this works

# response = requests.get(f'https://api.boardgameatlas.com/api/lists?username=trentellingsen&client_id={client_id}')
# this doesnt work


# response = requests.get('https://api.boardgameatlas.com/api/game/prices?game_id=6FmFeux5xH&client_id="client_id"')
# this does not work dont know why invalid client_id

# response = requests.get('https://api.boardgameatlas.com/api/game/prices?game_id=6FmFeux5xH&client_id=3Ya324qQb2')
# this works
# game_images = response.text[medium]
# print(game_images)

# print(data['images'])
# note that this works 
# print(data['images'][0])

# response = requests.get(f'{API_BASE_URL}/game/images?limit=1&client_id={client_id}')

# data = response.json()

# for result in data['images']:
    
#     print(result['medium'])
    
# note that this is going to return the medium images url


# print(response.text.images)
# Yay!!!! its working 


# games = requests.get(f'{API_BASE_URL}/game/images?limit=100&client_id={client_id}')
        
# games_data = games.json()

# for result in games_data['images']:
#     game_images = result['medium']

# games = requests.get(f'{API_BASE_URL}/game/images?limit=1&game_id&client_id={client_id}')
        
# games_data = games.json()

# for result in games_data['images']:
#     game_images = result['medium']
    
    # ipython board_game_mania.py
# note that this is returning 100 links for images which means you will need to loop through them probably in the html
    
    # print(game_images)
        
# games = requests.get(f'{API_BASE_URL}/search?name=Catan&client_id={client_id}')


# games_data = games.json()

# print(games_data)


            #  <!-- {% for i in range(0, len) %}
            #       <img src="{{game_images[i]}}"></img>
            #     {% endfor %} -->
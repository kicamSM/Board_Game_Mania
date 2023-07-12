// const API_BASE_URL = 'http://127.0.0.1:5000/'
// const API_BASE_URL = window.location.href
const API_BASE_URL = 'https://board-game-mania.onrender.com'

function generateGameHTML(game) {
    return `
    <div div class="container mt-4 mb-4 p-3 d-flex justify-content-center" data-id="{{ game_id }}"> 
        <div class="card p-4" style="width: 800px">
            <div>
            <h2 class="card-title">${game.name}</h1>
            </div>
            <div>
                <img src="${game.images.medium}" class="game-images card-img-top">
            <ul id="game-ul">
                <li class="info">Number of Players: ${game.players}</li>
                <li class="info">Playtime: ${game.playtime} mins</li>
                <li class="info">Artists: ${game.artists}</li>
                <li class="info">Primary Publisher: ${game.primary_publisher.name}</li>
                <li class="info">Primary Designer: ${game.primary_designer.name}</li>
          </ul>
            <div id="game-paragraph">
                <p class="card-text">${game.description_preview}</p>
            </div>
            </div>
            <a href="/users/${game.id}/log_play" class="button btn1 btn btn-success" style="font-size: 14px">Log Play</a>
            <a href="/games/${game.id}/delete" class="button btn1 btn btn-danger" style="font-size: 14px">Delete</a>
        </div> 
    </div>
    `;
    // NOTE HERE WE ARE JUST DYNAMICALLY CREATING THE HTML FOR THE GAMES 
  }

async function displayGames() {
    console.log('displayGames is running on users_games.js')
    // const response = await axios.get(`${BASE_URL}/games`);
    // console.log(API_BASE_URL)
    const response = await axios.get(`${API_BASE_URL}api/users/games`);
    // this we are pulling from the route in the API for games 
    console.log('response:', response)
    console.log(response.status);
    console.log('response.data:', response.data)
    console.log('response.data.games:', response.data.games)
    // const object = JSON.parse(response)
    // console.log('object:', object)
    // console.log(response)

    // console.log(response.data)

    for (let gameData of response.data.games) {
        console.log('gameData:', gameData)
          let newGame = $(generateGameHTML(gameData))
          $("#users-game-list").append(newGame);
      }
    // this is only passing one game data to html so you need to pass multiple games data 
    // console.log('gameData:', gameData)
    // console.log('gameData info:', gameData.primary_designer.name)
    // let newGame = $(generateGameHTML(gameData))
    // $("#users-game-list").append(newGame);

}
$(displayGames);

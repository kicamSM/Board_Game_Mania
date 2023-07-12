// const API_BASE_URL = 'http://127.0.0.1:5000/'
// const API_BASE_URL = window.location.href
const API_BASE_URL = 'https://board-game-mania.onrender.com'

// alert('loaded')

// console.log(API_BASE_URL)


function generateGameHTML(game) {
    return `
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
    `;
    // NOTE HERE WE ARE JUST DYNAMICALLY CREATING THE HTML FOR THE GAMES 
  }

async function displayGames() {
    console.log('displayGames is running')
    // const response = await axios.get(`${BASE_URL}/games`);
    // console.log(API_BASE_URL)
    const response = await axios.get(`${API_BASE_URL}api/games/${gameId}`);
    // this we are pulling from the route in the API for games 

    let gameData = response.data.games[0]
    console.log('gameData:', gameData)
    console.log('gameData info:', gameData.primary_designer.name)
    let newGame = $(generateGameHTML(gameData))
    $("#game-details").append(newGame);

}
$(displayGames);

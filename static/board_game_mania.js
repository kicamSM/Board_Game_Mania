// const API_BASE_URL = 'http://127.0.0.1:5000/'
const API_BASE_URL = 'https://board-game-mania.onrender.com'
// const API_BASE_URL = window.location.href




// alert('loaded')

console.log(API_BASE_URL)

function generateGameHTML(game) {
    return `
    <div class="col mb-3" data-id="${game.id}">
        <div class="card p-4 h-100">
          <div>
            <h2><a href="/games/${game.id}">${game.name}</a></h1>
          </div>
          <div>
             <a href="/games/${game.id}"><img src="${game.images.medium}" class="game-images"></a>
          </div>
        </div>
      </div>
    `;
    // NOTE HERE WE ARE JUST DYNAMICALLY CREATING THE HTML FOR THE GAMES 
  }

async function displayGames() {
    const response = await axios.get(`${API_BASE_URL}api/games`);
    // this we are pulling from the route in the API for games 

    for (let gameData of response.data.games) {
      console.log('gameData:', gameData)
      console.log('gameDataImages:', gameData.images.large)
        let newGame = $(generateGameHTML(gameData))
        $("#games-list").append(newGame);
    }

}


$(displayGames);
// displayGames()
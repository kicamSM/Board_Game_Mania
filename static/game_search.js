// const API_BASE_URL = 'http://127.0.0.1:5000/'
// const API_BASE_URL = window.location.href
const API_BASE_URL = 'https://board-game-mania.onrender.com/'

// alert('loaded')

// console.log(API_BASE_URL)

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
    console.log('displayGames is running in game_search.js')
    // const response = await axios.get(`${BASE_URL}/games`);
    // console.log(API_BASE_URL)
    // const response = await axios.get(`${API_BASE_URL}api/games/search`);
    // this we are pulling from the route in the API for games 
    console.log('response:', response)
    console.log(response.status);
    console.log('response.data:', response.data)
    console.log('response.data.games:', response.data.games)
    // const object = JSON.parse(response)
    // console.log('object:', object)
    // console.log(response)

    // console.log(response.data)

    // for (let gameData of response.data.games) {
    //   console.log('gameData:', gameData)
    //   console.log('gameDataImages:', gameData.images.large)
    //     let newGame = $(generateGameHTML(gameData))
    //     $("#game-search").append(newGame);
    // }

}


$(displayGames);
// displayGames()
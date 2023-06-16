const API_BASE_URL = 'http://127.0.0.1:5000/'

function generateGameHTML(game) {
    return `
    <div>
      <h2 class="card-title">${game.name}</h1>
      <div>
        <img src="${game.images.medium}" class="game-images card-img-top">
      </div>
    </div>`

}


async function retrieveGameResults() {
    console.log('retrieveGameResults is running in match_results.js')
    // const response = await axios.get(`${BASE_URL}/games`);
    // console.log(API_BASE_URL)
    const response = await axios.get(`${API_BASE_URL}api/results`);
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
      console.log('gameDataImages:', gameData.images.large)
        let newGame = $(generateGameHTML(gameData))
        $("#games-list").append(newGame);
    }

}


$(displayGames);
$(displayGames);
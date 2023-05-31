const API_BASE_URL = 'http://127.0.0.1:5000/'

alert('loaded')

// console.log(API_BASE_URL)


function generateGameHTML(game) {
    return `
      <div data-id=${game.id}>
        <h1>This is the Generated html</h1>
        <li>
       ${game}
        </li>
      </div>
    `;
    // NOTE HERE WE ARE JUST DYNAMICALLY CREATING THE HTML FOR THE GAMES 
  }

async function displayGames() {
    console.log('displayGames is running')
    // const response = await axios.get(`${BASE_URL}/games`);
    // console.log(API_BASE_URL)
    const response = await axios.get(`${API_BASE_URL}/games`);
    // this we are pulling from the route in the API for games 
    console.log(response)
    console.log(response.status);

    // const object = JSON.parse(response)
    // console.log('object:', object)
    // console.log(response)

    // console.log(response.data)

    for (let gameData of response.data) {
        let newGame = $(generateGameHTML(gameData))
        $("#games-list").append(newGame);
    }

}
$(displayGames);
// displayGames()
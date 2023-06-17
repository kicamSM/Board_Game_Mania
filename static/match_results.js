const API_BASE_URL = 'http://127.0.0.1:5000/'

// console.log(matches['win'])

function generateGameHTML(game, idCount, wins, loss) {
    return `

    <div class="col mb-3">
      <div class="card p-4 h-100">
        <div>
          <h1 class="card-title">${game.name}</h1>
          <div>
            <a href="/games/${game.id}"><img src="${game.images.medium}" class="game-images"></a>
          </div>
          <div class="card-body">
            <h3>Total Number of Plays: ${idCount}</h3>
            <p> Total Number of Wins: ${wins} Total Number of Losses: ${loss}
            </p>
          </div>
        </div>
      </div>
    </div>`
  

}

async function retrieveGameResults(idCounts, wins) {
    console.log('retrieveGameResults is running in match_results.js')

    // let wins = 0;
    // let losses = 0;
    
    // for(let i = 0; i < matches.length; i++ ) {
    //   matches[i]
    //   console.log('length:', matches.length)
    // }
    // const response = await axios.get(`${BASE_URL}/games`);
    // console.log(API_BASE_URL)
    const response = await axios.get(`${API_BASE_URL}api/results`);
    
    // for (let gameData of response.data.games) {

    for(let i = 0; i < response.data.games.length; i++) {
      // console.log('gameData:', gameData)
      // console.log('gameDataImages:', gameData.images.large)
        // let newGame = $(generateGameHTML(gameData, idCounts))
        let game_data = response.data.games[i]
        let num_plays = Object.values(idCounts)[i]
        let num_wins = Object.values(wins)[i]
        let num_losses = (num_plays - num_wins)
        // let newGame = $(generateGameHTML(response.data.games[i], Object.values(idCounts)[i], Object.values(wins)[i],  ))
        let newGame = $(generateGameHTML(game_data, num_plays, num_wins, num_losses))
        $("#results-list").append(newGame);
    }

}

function countGameIds() {
  let idCounts = {};
  let wins = {}
    for(let i = 0; i < matches.length; i++) {
    
      for(let j = 0; j < game_ids_no_dup.length; j++) {
      let id = game_ids_no_dup[j]; 
    
        if(id == matches[i]['game_id']) {
        idCounts[id]++; 
        } else {
          idCounts[id] = 1
          console.log('id', id)
          console.log('matches[i]["game_id"]:', matches[i]['game_id'])
        }

        if(id == matches[i]['game_id'] && matches[i]['win'] == true) {
          wins[id]++; 
          } else {
            wins[id] = 1

      }
    }
  }
  console.log('idCounts:', idCounts)
  console.log('wins:', wins)
  $(retrieveGameResults(idCounts, wins))
}

// ********************************************************************
 // for( const match in matches) {
   // matches.forEach(countIds());{

       // if (game_ids_no_dup == match.game_id) {
      //  if (game_ids_no_dup == matches[i]['game_id']) {
      // if (game_ids_no_dup.includes(matches[i]['game_id'])) {





// ********************************************************************

  // console.log('matchesArray:', matchesArray)
  // matchesArray = Object.values(matches)
  // console.log('matchesArray:', typeof matchesArray)


  // console.log(matchesArray)s
  // const result = matchesArray.group(({ game_id }) => game_id);
  // console.log(result)


  // const groups = [];
  // for (const game in matches) {
  //   const id = game.game_id;
  //   const win = game.win; 
  //   if (!groups[id]) {
  //     groups[id] = [];
  //   }
  //   groups[id].push(game);
  // }
 



// const groupByCategory = matches.groupBy(matches => {
//   console.log('matches.game:', matches.game)
//   return matches.game_id;
// });

// var result = matches.reduce((x, y) => {

//   (x[y.game_id] = x[y.game_id] || []).push(y);

//   console.log(x)
//   return x;

// }, {});


// $(groupByCategory)
// $(result)
$(countGameIds)
// $(retrieveGameResults);
// $(groupByGame_ids)
// $(displayGames);
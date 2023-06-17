const API_BASE_URL = 'http://127.0.0.1:5000/'


function generateGameHTML(game, idCount, wins, loss) {
    return `

    <div class="col mb-3">
      <div class="card p-4 h-100">
        <div>
          <h1 class="card-title">${game.name}</h1>
          <div>
            <a href="/matches"><img src="${game.images.medium}" class="game-images"></a>
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

    const response = await axios.get(`${API_BASE_URL}api/results`);
    

    for(let i = 0; i < response.data.games.length; i++) {
   
        let game_data = response.data.games[i]
        let num_plays = Object.values(idCounts)[i]
        let num_wins = Object.values(wins)[i]
        let num_losses = (num_plays - num_wins)

        let newGame = $(generateGameHTML(game_data, num_plays, num_wins, num_losses))
        $("#results-list").append(newGame);
    }

}

function countGameIds() {
  let idCounts = {};
  console.log('idCounts:', idCounts)
  let wins = {}

    for(let i = 0; i < matches.length; i++) {
    
      for(let j = 0; j < game_ids_no_dup.length; j++) {
      let id = game_ids_no_dup[j]; 
        console.log('matches[i]["game_id"]:', matches[i]['game_id'])

        if (typeof idCounts[id] === "number" || typeof idCounts[id] == 'undefined') {
          console.log('INSIDE IF TYPEOF idCounts[id]', idCounts[id])
          if (isNaN(idCounts[id])) {
            idCounts[id] = 0;
            console.log('INSIDE IF IF (X2) TYPEOF idCounts[id]', idCounts[id])
          }
        }
        console.log('LOOK AT THIS', typeof wins[id])

        if (typeof wins[id] == "undefined") {
          console.log('INSIDE IF TYPEOF wins[id]', wins[id])
          if (isNaN(wins[id])) {
            wins[id] = 0;
            console.log('INSIDE IF IF (X2) TYPEOF wins[id]', wins[id])
          }
        }


        if(id === matches[i]['game_id']) {

          // if (typeof idCounts[id] === "number") {
          //   console.log('INSIDE IF TYPEOF idCounts[id]', idCounts[id])
          //   if (isNaN(idCounts[id])) {
          //     idCounts[id] = 0;
          //     console.log('INSIDE IF IF (X2) TYPEOF idCounts[id]', idCounts[id])
          //   }
          // }

          // if (typeof matches[i]['win'] === "number") {
          //   console.log('INSIDE IF TYPEOF matches[i]["win"]', idCounts[id])
          //   if (isNaN(matches[i]['win'])) {
          //     matches[i]['win'] = 0;
          //     console.log('INSIDE IF IF (X2) TYPEOF matches[i]["win"]', idCounts[id])
          //   }
          // }
        
          console.log('id:', id)
          console.log('if(id == matches[i]["game_id"])', id )
          console.log('CHECK THIS idCounts[id]', idCounts[id])
          idCounts[id]++; 
          console.log('AGAINST THIS idCounts[id]', idCounts[id])
          // SO MY UNDERSTANDING OF THIS RIGHT NOW IS THAT BECAUSE THE SECOND ID IN LIST DOES NOT EQUAL THE FIRST ID IN LIST WE THEN GO TO THE ELSE STATEMENT WHICH RESETS THE LIST OF THE FIRST ID TO 1... DONT WANT THIS TO HAPPEN!!!!
        }
          // } else {
          //   idCounts[id] = 1
          //   console.log('IS THIS IF STATEMENT RUNNING? idCounts::',  idCounts)
          //   console.log('id', id)
            
          //   console.log('matches[i]["game_id"]:', matches[i]['game_id'])
          // }

        if(id === matches[i]['game_id'] && matches[i]['win'] == true) {
          wins[id]++; 
          // } else if (typeof wins[id] === "number") {
          //   console.log('INSIDE IF TYPEOF wins[id]', wins[id])
          //   if (isNaN(wins[id])) {
          //     wins[id] = 0;
          //     console.log('INSIDE IF IF (X2) TYPEOF idCounts[id]', idCounts[id])
            }
          // } else {
          //   idCounts[id]++
            
          // }

        // if(matches.length == 1) {
        // console.log('third if statement is running')
        // idCounts[id] = 1;

        // console.log('LAST IF STATEMENT idCounts:', idCounts)
        //   if(matches[i]['win'] == true) {
        //   wins[id] = 1; 
        //   console.log('wins if statement :', wins)
        //   } else {
        //   wins[id] = 0;
        //   // console.log('wins else statement:', wins)
        //   // note this is having issues still because if you run the same game twice it game_ids_no_dup length is still 1 so it resets again. 
        //  }
        // }
      }
    }
  $(retrieveGameResults(idCounts, wins))
}

// note=


$(countGameIds)

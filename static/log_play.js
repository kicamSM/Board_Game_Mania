

// $('form').live('submit', function(){
//     $.post($(this).attr('action'), $(this).serialize(), function(response){
//         $(generateGameHTML)
//     },'json');
//     return false;
//  });

//  function generateGameHTML() {
//     for(let i=0;r<parseInt(players ,10);i++) {

//         `<input type="text">hello name="Player {i}><br>`
      
//        let entryDiv = document.getElementById('name-entry').insertRow(i);

//     }

//  }

// $('#player-count').on('submit', function(e) {
//   e.preventDefault();
//   console.log('functione is running')
//   // $(createForm);
//   let num_players = document.getElementById("player-count").value
//   console.log(num_players)
  
// });

// console.log(players)


function createForm() {
    console.log('createForm in log_play.js is running')
    console.log(players)
    console.log('another console.log is running')

    console.log(players)
    // players is not running 
    plyrs = players
    console.log(plyrs)
    let form = document.createElement("form");
    form.action = "/log_play/name/score";
    form.method = "post";

    // for (let i = 1; players <= i; i++) {
    //     var inputName = document.createElement("input");
    //     inputName.type = "text";
    //     inputName.name = "player" + i + "_name";
    //     inputName.placeholder = "Player " + i + " name";

    //     // var inputAge = document.createElement("input");
    //     // inputAge.type = "number";
    //     // inputAge.name = "player" + i + "_age";
    //     // inputAge.placeholder = "Player " + i + " age";
    
    //     form.appendChild(inputName);
        // form.appendChild(inputAge);
      }

      // var submitButton = document.createElement("input");
      // submitButton.type = "submit";
      // submitButton.value = "Submit";
    
      // form.appendChild(submitButton);
    
      // // document.body.appendChild(form);
      // $("#name-div").append(form)
    // }

    // var n = parseInt(document.querySelector("input[name=n]").value);

// $(createForm);




// async function displayGames() {
//     console.log('displayGames is running in board_game_mania.py')
//     // const response = await axios.get(`${BASE_URL}/games`);
//     // console.log(API_BASE_URL)
//     const response = await axios.get(`${API_BASE_URL}api/games`);
//     // this we are pulling from the route in the API for games 
//     console.log('response:', response)
//     console.log(response.status);
//     console.log('response.data:', response.data)
//     console.log('response.data.games:', response.data.games)
//     // const object = JSON.parse(response)
//     // console.log('object:', object)
//     // console.log(response)

//     // console.log(response.data)

//     for (let gameData of response.data.games) {
//       console.log('gameData:', gameData)
//       console.log('gameDataImages:', gameData.images.large)
//         let newGame = $(generateGameHTML(gameData))
//         $("#games-list").append(newGame);
//     }

// }

// $(displayGames);
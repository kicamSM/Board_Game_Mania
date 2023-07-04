// console.log('name_entry.js is running!')

// console.log(num_players)
// console.log(g_name)
// console.log(typeof num_players)

let intPlayers = parseInt(numPlayers)
// console.log(typeof int_players)

function createForm() {
    let form = document.createElement("form");
    form.action = `/log_play/${gameName}/${gameId}/score`;
    form.method = "post";
    if(intPlayers === 1) {
      intPlayers++;
      // note this is because 
    }

    for (let i = 1; i <= intPlayers; i++) {
        let inputName = document.createElement("input");
        inputName.type = "text";
        inputName.name = "player" + i + "_name";
        inputName.placeholder = "Player " + i + " name";
        inputName.className = "name-fields form-control"

        let inputEmail = document.createElement("input")
        inputEmail.type = "email";
        inputEmail.name = "player" + i + "_email";
        inputEmail.placeholder = "Player " + i + " email";
        inputEmail.className = "name-fields form-control"
        inputEmail.required = true
        
        if(i == 1) {
            inputName.value = username
            inputEmail.value = email
        }
     
    
        form.appendChild(inputName);
        form.appendChild(inputEmail)
        // form.appendChild(inputAge);
      }

      var submitButton = document.createElement("input");
      submitButton.type = "submit";
      submitButton.value = "Create Scoreboard";
      submitButton.className = "button btn1 btn btn-success"
      submitButton.style = "font-size: 14px"

    //   <a href="/games/{{game_id}}/add" class="button btn1 btn btn-success" style="font-size: 14px">Create Scoreboard</a>
    //   this is appending which makes me think the form in theory is appending
    
      form.appendChild(submitButton);
    
      // document.body.appendChild(form);
      $("#name-entry").append(form)
    }

    // var n = parseInt(document.querySelector("input[name=n]").value);

$(createForm);
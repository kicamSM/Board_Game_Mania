
let intPlayers = parseInt(numPlayers)

function createForm() {
    let form = document.createElement("form");
    form.action = `/log_play/${gameName}/${gameId}/score`;
    form.method = "post";
    if(intPlayers === 1) {
      intPlayers++;
      // This is because if you are playing a one person game you play against the board so the board will have a place to be scored.
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
      }

      let submitButton = document.createElement("input");
      submitButton.type = "submit";
      submitButton.value = "Create Scoreboard";
      submitButton.className = "button btn1 btn btn-success"
      submitButton.style = "font-size: 14px"
    
      form.appendChild(submitButton);
    
      // document.body.appendChild(form);
      $("#name-entry").append(form)
    }

$(createForm);
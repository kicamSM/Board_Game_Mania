// console.log('name_entry.js is running!')

// console.log(num_players)
// console.log(g_name)
// console.log(typeof num_players)

let int_players = parseInt(num_players)
// console.log(typeof int_players)

function createForm() {
    let form = document.createElement("form");
    form.action = `/log_play/${g_name}/${game_id}/score`;
    form.method = "post";

    for (let i = 1; i <= int_players; i++) {
        let inputName = document.createElement("input");
        inputName.type = "text";
        inputName.name = "player" + i + "_name";
        inputName.placeholder = "Player " + i + " name";
        inputName.className = "name-fields form-control"
        
        if(i == 1) {
            inputName.value = username
        }
        // var inputAge = document.createElement("input");
        // inputAge.type = "number";
        // inputAge.name = "player" + i + "_age";
        // inputAge.placeholder = "Player " + i + " age";
    
        form.appendChild(inputName);
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
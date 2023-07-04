
function generateHeaderHTML() {
    // let header = document.getElementById('myTable').insertRow(0);
    let table = document.getElementById('myTable');
    table.className = 'table'
    let header = table.createTHead()
    header.className = 'thead'
    let row = header.insertRow(0)

    namesArray.forEach(function (name, index) {
        let cell = row.insertCell()
        cell.id = (`head-${index}`)
        cell.innerHTML = name
    })

   $(generateBodyHTML);

}


function promptNumber() {
    let number = prompt("Input number of turns if known. Otherwise, press ok.", 1)
    let input = /^[0-9]+$/
    if (input.test(number)) {
        if(number === '0' ) {
            console.log('number', number)
            number ++; 
        }
        return number
    } else {
        let number = 1;
        return number 
    }
  }

function generateBodyHTML() {
    row_num = promptNumber()

    console.log('row_num', row_num)
    console.log('type row_num', typeof(row_num))

    col_num = namesArray.length;
    
        for(let row = 0; row < row_num; row++) {
            let table = document.getElementById('myTable');
            let body = table.createTBody();
    
            body.id = 'tbody'
         
            let rowEle = body.insertRow()
 
            for(let cell = 0; cell < parseInt(col_num,10); cell++) {
                let cellEle = rowEle.insertCell(cell);
                // cellEle.id = (`${row}-${cell}`)
                if(cell = namesArray.indexOf(namesArray[cell])) {
                    cellEle.className = `Player${cell}`
                }
           
                cellEle.setAttribute('contenteditable', 'true')
            
                $('[contenteditable="true"]').keypress(function(e) {
                    var x = event.charCode || event.keyCode;
                    // console.log('x:', x)
                    if (isNaN(String.fromCharCode(e.which)) && x!=46 || x===32 || x===13 || (x===46 && event.currentTarget.innerText.includes('.'))) e.preventDefault();
                    // console.log(currentTarget.id)
            });
        }
    }
    $(generateFooterHTML)
}

function generateFooterHTML() {
    console.log('generateFooterHTML is running in score.js')
    row_num = 1
    col_num = (namesArray.length);
    // console.log(col_num)
    let table = document.getElementById('myTable');
    let footer = table.createTFoot();
    let rowEle = footer.insertRow()

    for(let cell = 0; cell < col_num; cell++) {
        //  let y = x.insertCell(c);
    let cellEle = rowEle.insertCell();
    // console.log(cellEle)
    cellEle.id = (`foot-${cell}`)
    cellEle.className = 'footer'
    cellEle.innerHTML="Score"; 
    }
}


function addRow() {
    body = document.getElementById('tbody')
    table = document.getElementById('myTable')
    let col_num = namesArray.length;
    let newRow = document.createElement('tr')

    for(let cell = 0; cell < parseInt(col_num,10); cell++) {
            let cellEle = newRow.insertCell(cell);
            console.log('cellEle', cellEle)
            newRow.appendChild(cellEle)

            if(cell = namesArray.indexOf(namesArray[cell])) {
                cellEle.className = `Player${cell}`
            }
            console.log('body', body)
            body.appendChild(newRow)

            cellEle.setAttribute('contenteditable', 'true')
        
            $('[contenteditable="true"]').keypress(function(e) {
                var x = event.charCode || event.keyCode;
                // console.log('x:', x)
                if (isNaN(String.fromCharCode(e.which)) && x!=46 || x===32 || x===13 || (x===46 && event.currentTarget.innerText.includes('.'))) e.preventDefault();
        })
    }
}

function sumTotalTable() {

    let rows = $("#myTable").find("tbody>tr");
    let footers = $(".footer")
    let sumArray = []

    for (let i = 0; i < rows[0].cells.length; i++) {
        let sum = 0; 

        for (let j = 0; j < rows.length; j++) {
            console.log('rows.length:', rows.length)
            let cell = rows[j].cells[i];
            // j is the index of the row 
            // i is the index of the cell
            // basically we are taking the table body back apart the way we put it together
            // console.log('cell.innerText:', cell.innerText)
            // console.log('typeof(cell.innerText):', typeof(cell.innerText))
            // this is returning the string 
            // cells are going to be individual cells how many per row 
            //j is internal row num wherease cell is internal cell num
            if (!isNaN(parseInt(cell.textContent, 10))) {
                sum += parseInt(cell.textContent, 10);
            }
        }

        footers[i].textContent = sum;
        sumArray.push(sum)
        console.log('sumArray', sumArray)
    }
    document.getElementById('win').style = "font-size: 14px" 
    console.log(document.getElementById('win'))
    document.getElementById('form-route').action = `/log_play/${game_id}/save/${namesArray}/${sumArray}`
    $(declareWinOrLoss)
}

function declareWinOrLoss() {

    let userTotalObj = document.getElementById("foot-0")
    let userTotalStr = userTotalObj.textContent
    let userTotal = parseInt(userTotalStr)
    let totalsObj = document.getElementsByClassName("footer")
  
    for(let i = 1; i < totalsObj.length; i++) {

        let total = parseInt(totalsObj[i].innerText, 10);
        let input = document.getElementById('win')
        console.log('input', input)

        if(total >= userTotal) {
            console.log(false)
            let win = false
            input.setAttribute("value", `${win}`)
            }
        else {
            console.log(true)
            let win = true
            input.setAttribute("value", `${win}`)
        }
    }
}

$(generateHeaderHTML)

//  async function postScoreToRoute(sumArray) {

//     const res = await axios.post(`http://localhost:5000/(/log_play/${game_id}/save/${namesArray}`, {scores: { sumArray }})
//     console.log(res)
 
// }

// function postScoreToRoute(sumArray) {
//     const axios = require('axios');

//     const url = `http://localhost:5000/(/log_play/${game_id}/save/${namesArray}`;

//     console.log(url)
//     const data = {
//     name: 'John Doe',
//     age: 30
//     };

//     axios.post(url, data)
//     .then(response => {
//     console.log(response.data);
//     })
//     .catch(error => {
//     console.error(error);
//     });
// }

// function postScoreToRoute(sumArray) {
//     console.log('sumArray in postScoreToRoute:', sumArray)
//     // response = requests.post('http://localhost:5000/results/score_data', sumArray)

//     response = requests.post(`/log_play/${game_id}/${namesArray}`, json.dumps(sumArray))

// }

// async function postScoreToRoute(sumArray) {
//     console.log('sumArray in postScoreToRoute:', sumArray)
//     // response = requests.post('http://localhost:5000/results/score_data', sumArray)

//     const response = await fetch(`/log_play/${game_id}/${namesArray}`, {
//         method: 'POST', 
//         body: `text=${text}`, 
//         headers: {
//             'Content-Type': 'application/x-www-for-urlencoded',
//         },
//         });
//         const json = await response.json();
//         return json.label === 'pos'
//     }


// async function saveResults(win) {
//     const res = await axios.post('/log_play/${game_id}/save', {
//         Win: win, Num_players: num_players
//     })
//     console.log(res)
// }


// function createUploadForm(win){
//     // let userName = localStorage.getItem("username");
//     let form = document.createElement("form");
//     form.setAttribute("method", "POST");
//     form.setAttribute("enctype", "multipart/form-data");
//     form.setAttribute("action", "/log_play/${game_id}/save");

//     //create hidden input element for user ID
//     let userID = document.createElement("input");
//     userID.setAttribute("type", "hidden");
//     userID.setAttribute("win", "win");
//     userID.setAttribute("name", "win");
//     userID.setAttribute("value", win);

// }
        
       

// *****************************************************************************************
        // for(let i = 0; i < namesArray.length; i++) {
        //     // sumVal = + parseInt(table.columns[i].cells.innerHTML)
        //     // console.log(sumVal)
        //     // columns = $(`.${namesArray[i]}`)
        //     // columnshtml = document.getElementsByClassName(`.${namesArray[i]}`)

        //     myArray = []
        //     // let Player[i] = [];

        //     // let col = $(`.${namesArray[i]}`)
        //     // console.log
        //     mArray = []
        //     columns = $(".Player1")
        //     // columnsText = columns[i].innerText
        //     console.log('columnsText:', columnsText)
        //     console.log('columns[i]:', columns[i])
        //     console.log('testing InnerText:', columns[1].innerText)
        //     console.log('testing textContent:', columns[1].textContent)
        //     console.log('testing InnerHTML:', columns[1].innerHTML)
        //     // this is retruning the inside fo the collums fyi
        //     myArray.push(columns.innerHTML)
        //     console.log(mArray)
        //     // this worked to get the elements 
        //     console.log('col:', columns)
        //     rows_w = $("tbody td .Player2")
        //     console.log('rows_w:', rows_w)
        //     rows = $(`.${namesArray[i]} tbody tr`)
        //     console.log('rows:', rows)
        //     console.log('before jquery')
        //     $( document ).ready( function() {
        //         var sum_total = 0;
        //         $(`.namesArray[${i}] tbody tr`).each(function(i) {
        //             console.log($(`.${namesArray[i]} tbody tr`))
        //             // console.log('i:', i)
        //             // console.log('jquery is running')
        //             // console.log(index)
        //       sum_total += $(this).children().eq(i).text() * 1;
        //     });
        //     console.log('sum_total:', sum_total)

        //     $( `td #foot-${i}` ).text( sum_total );
        
        // });
    
        // this is the last code I was running ABOVE 
        // *************************************************************************************

            // let columnsObject = document.getElementsByClassName(namesArray[i])
            // this in theory should return as many arrays as there are names which is probably my problem. 
            // console.log('columnsObject:', columnsObject)

            // myArray.push(columnsObject[i].innerHTML)
            // console.log('myArray', myArray)

            // let columnsVal = columnsObject[i].innerHTML.push(Player[i])
            // console.log('columnsObject1:', columnsObject)
            // col1 = columnsObject[0]
            // console.log('col1:', col1)
            // colTxt = col1.innerHTML
            // console.log('colTxt:', colTxt)
            // col1Val = col1.innerHTML
            // let columnsArray[i] = columnsNodeList[i]
            // columnsText[i] = columnsArray[i].innerHTML
            // console.log(Player[i])

            // player2col = document.getElementsByClassName(namesArray[1])
            // player2text = player2col[0].innerHTML
            // console.log('columnsObject1:', columnsObject)
            // console.log('columns:', columns)
            // console.log('col1:', col1)
            // console.log('col1Val:', col1Val)
        
        // }
        // console.log(player2text)
            // console.log('columnsObject2:', columnsObject)
        // console.log('columnsArray:', typeof(columnsArray))
        // console.log('columnsText:', columnsText)

    // }






// now you want to say if all columns have been edited when there is only  row, then an additional row. Continue to do this until complete has been clicked




        // if (y.id[0] == 0) {
        //     // console.log(y.id[0][1])
        //     console.log('if statement is running')
            
        //     for(i = 0; i <namesArray.length; i++) {
        //     console.log('for statement is running')
        // //     console.log('namesArray.length:', namesArray.length)
        //         console.log('i:', i)
        //         console.log('namesArray[i]:', namesArray[i])
        //         let id = (`0, ${i}`)
                // my understanding of this is that i should be equal to 0, 1, and 2 becuase of the for loop 
                // i = 0 (i starts at zero) i < namesArray.length if names array.length = 3 (i will stop at 2)
                // i++ (i will continue in incriments of one)
                // this should give me three ids 
                // console.log(id)

                // document.getElementById(id).innerHTML = namesArray[i]
                // this is getting the element by id (three ids) and should be setting the value as the value of namesArray index of i 
            // }

            // document.getElementById(id).innerHTML = namesArray[i]
            // if this goes outside the loop all items are returning in the loop no html is getting set

            //   }
            //   document.getElementById(id).innerHTML = namesArray[i]
            // id is not defined here


        // y.innerHTML="Row-"+r+" Column-"+c; 
            // y.innerHTML = y.id
        // }
//      }

//  }
//  $(generateGameHTML);



// ****************************************************************************

// function generateGameHTML() {
//     console.log('generateGameHTML is running in score.js')
//     for(let i=1; i < players; i++) {
//         let tr = document.createElement('tr');   

//         let td1 = document.createElement('td');
//         let td2 = document.createElement('td')

//         var text1 = document.createTextNode('Text1');
//         var text2 = document.createTextNode('Text2');
    
//         td1.appendChild(text1);
//         td2.appendChild(text2);
//         tr.appendChild(td1);
//         tr.appendChild(td2);
    
//         table.appendChild(tr);
//     }
//     document.body.appendChild(table);

// }

// ***************************************************************************************

    // let headCell = `<td class="headCell">This is my headcell</td>`
//     let arrayOfTDs = []
//     for(let i=0; i < players; i++) {
//         let headCell = `<td class="headCell" style="height=50px">This is my headcell</td>`
//         // console.log(players)
//         arrayOfTDs.push(headCell) 
//         // console.log(arrayOfTDs)
//     }
//     // return arrayOfTDs

//     console.log(arrayOfTDs)
//     let tr = document.createElement('tr');
//     arrayOfTDs.forEach(function(td) {
//         // Parse the HTML string into a DOM node
//         console.log('td:', td)
//         let tempTd = document.createElement('td');
//         tempTd.classList.add('headCell')
//         // document.getElementsByClassName('headCell').style.color = "red"
//         // tempDiv.className = "headCell"
//         console.log('tempTd1:', tempTd)
//         // create a temporary div element 
//         tempTd.innerHTML = td;
//         console.log('tempTd2:', tempTd)
//         let tdElement = tempTd.firstChild;
//         console.log('tdElement:', tdElement)
//         // console.log(tdElement)
      
//         // Append the td to the tr
//         // tr.appendChild(tdElement);
//         tr.appendChild(tdElement);
        
//         $("#table-head").append(tr);
//     });
// }

// ************************************************************************************
// above was not creating multiple tds only one with multiple inputs inside the td 

// for(let i = 0; i < players.length; i++) {
//     let scoreboard = `<tr id="head">
//     <td class="headCell"></td>
//     <td class="headCell"></</td>
//     <td class="headCell"></</td>
//     <td class="headCell"></</td>
//     <td class="headCell"></</td>
//     <td class="headCell"</</td>
//   </tr>`
// // thead.innerHTML = rowHead;
// }
// }
//     for(let i = 0; i < 5; i++) {
// let rowBody = `<tr id="body">
//                   <td class="bodyCell null" id="${0}-${i}">${'?'}</td>
//                   <td class="bodyCell null" id="${1}-${i}">${'?'}</td>
//                   <td class="bodyCell null" id="${2}-${i}">${'?'}</td>
//                   <td class="bodyCell null" id="${3}-${i}">${'?'}</td>
//                   <td class="bodyCell null" id="${4}-${i}">${'?'}</td>
//                   <td class="bodyCell null" id="${5}-${i}">${'?'}</td>
//                 </tr>`
//       tbody.innerHTML += rowBody; 

//               }
      
//     // NOTE HERE WE ARE JUST DYNAMICALLY CREATING THE HTML FOR THE GAMES 
//   }

// you will need this function to append the score-board but you wont need it to grab data from a route

// async function displayGames() {
//     console.log('displayGames is running in score.js')
//     // // const response = await axios.get(`${BASE_URL}/games`);
//     // // console.log(API_BASE_URL)
//     // const response = await axios.get(`${API_BASE_URL}api/games`);
//     // // this we are pulling from the route in the API for games 
//     // console.log('response:', response)
//     // console.log(response.status);
//     // console.log('response.data:', response.data)
//     // console.log('response.data.games:', response.data.games)
//     // // const object = JSON.parse(response)
//     // // console.log('object:', object)
//     // // console.log(response)

//     // // console.log(response.data)

//     // for (let gameData of response.data.games) {
//     //   console.log('gameData:', gameData)
//     //   console.log('gameDataImages:', gameData.images.large)
//         // let scoreboard = $(generateGameHTML(players))
//         let tds = $(generateGameHTML(players))
//         // let header = headerArray.replace('[]', '')
//         // console.log(header)

//         $("#table-head").append(tds);
//     }

// }


// $(decodeHtml);
// $(displayGames);


// ************************************************************************************************
// notes 
// ************************************************************************************************


// const API_BASE_URL = 'http://127.0.0.1:5000/'

// alert('loaded')

// console.log(API_BASE_URL)

// console.log(namesHTML)
// how to decode html character reference in javascript
// the names list is encoding ' character in the array wich is why I end up with some like this
// [&#39;a&#39;, &#39;Tom&#39;, &#39;Ben&#39;, &#39;Sasha&#39;]
// json = JSON.stringify(namesList)

// json = JSON.parse(namesList)

// ************************************************************************************************
 
        //   if (y.id[0] == 0) {
        //     console.log('if statement is running')
        //     for(i = 0; i <= namesArray.length; i++) {
        //     console.log('namesArray[i]:', namesArray[i])
        //     console.log('namesArray[2]:', namesArray[2])
        //     console.log
        //         for(let y = 0; y < y.length; y++)
        //             y.innerHTML = namesArray[i]
        //     // y.innerHTML = namesArray[2]
        //     // console.log(y.innerHTML)
        //     }
        //   }


        // console.log(json)
// ************************************************************************************************

// function decodeHtml(namesList) {
//     var txt = document.createElement("textarea");
//     txt.innerHTML = namesList;
//     // return txt.value;
//     console.log(txt.value)   
// }
// console.log(txt.value)

// function decodeHtml(namesHTML) {
//     let namesList = $("<div/>").html(namesHTML).text();
//     console.log('namesList1:', namesList)

//     generateGameHTML(namesList)
// }
// console.log($("<div/>").html(namesHTML).text())
// this is working to decode the html
// let num = sessionStorage.getItem('num_players')
// console.log('num:', num)

// let names = sessionStorage.getItem('names_list')
// console.log(names)
// according to this we are not getting anything from session storage

// function decodeHtml(namesHTML) {
//         // let namesList = $("<div/>").html(namesHTML).text();
//         // this is not working setting it as a variable
//         // console.log('namesList1:', namesList)

//         return $("<div/>").html(namesHTML).text()
//         generateGameHTML($("<div/>").html(namesHTML).text())
//     }
//     console.log(typeof($("<div/>").html(namesHTML).text()))

// ************************************************************************************************
      //         document.getElementById(`0, ${(y.id[0][i])}`).innerHTML = namesArray[i]
            //    firstYID = 0, (y.id[0][`${i}`])
            //  firstYID = document.getElementById(`0, ${(y.id[0][i])}`)
            // firstYID = document.getElementById('0, 0')
            // this one came back use this format as a string for the id 
            // y.innerHTML = 'this is ys inner html'
            // console.log('firstYID:', firstYID)
            // console.log('yById:', document.getElementById(0,0))
            // console.log('yById:', $('#0, 0'))
            // y.getElementById(0,(y.id[0][`${i}`])).innerHTML = namesArray[i]


                    // }
                    // if(y.id[0][i]) {
                    //     y.innerHTML = namesArray[i]
                    // }
                // console.log('namesArray[i]:', namesArray[i])
                // console.log('namesArray[2]:', namesArray[2])
                // console.log
                // namesArray.forEach(ele, i) => {
                //     y.innerHTML = namesArray[i]
                // }
                    // for(let y = 0; y < y.length; y++)
                    //     y.innerHTML = namesArray[i]
                // y.innerHTML = namesArray[2]
                // console.log(y.innerHTML)
                // }

// *****************************************************************************************************
      
            //     $(document).ready(function () {
            //         $('#bt').click(function () {
            //             $('0-1')
            //                 .attr('contenteditable', 'true')
            //                 .focus();
            //         });
            //     });
            // }
        
            // }

                    // $(cellEle).keypress( "click", function(event) {
                // // event.target.attr('contenteditable', 'true')
                // if (isNaN(String.fromCharCode(e.which))) e.preventDefault();
                // });

            // $(cellEle).on( "click", function(event) {
            //     // event.target.attr('contenteditable', 'true')
            //     ele = document.getElementById(event.target.id)
            //     console.log(ele)
            //     ele.attr('contenteditable', 'true')
            //     alert( $( this ).html() );
            //     console.log( event.target );
            
            // } );
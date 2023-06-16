


// console.log('namesArray in score.js:', namesArray)

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
// breaking this up because the issue of having too many for loops nested is causing problems. 

// function generateButtonHTML(win, num_players, game_id) {
//     console.log('generate button html is running')
//     console.log('win:', win)
//     return `
//     <form action="/log_play/${game_id}/save" method="POST">
//         <input type="hidden" name="win" id="win" value="${win}"></input>
//         <input type="hidden" name="num_players" id="num_players" value="${num_players}"></input>
//         <button class="button btn1 btn btn-success" type="submit" style="font-size: 14px">Save</button>
//     </form>`
   
// }

function generateBodyHTML() {
    // console.log('generateGameHTML is running in score.js')
    row_num = window.prompt("Input number of turns if known. Otherwise, press ok", 1);

    col_num = namesArray.length;
    // console.log(col_num)
    // console.log(cn)
    // console.log(players)
    // cn = window.prompt("Input number of columns",1);
      
    //  for(let r = 0; r < parseInt(row_num, 10); r++) {
        for(let row = 0; row < row_num; row++) {
            let table = document.getElementById('myTable');
            let body = table.createTBody();
            // body.id = 'tbody'
            // body.setAttribute(contenteditable)
            body.className = 'tbody'
            // console.log(body)
            let rowEle = body.insertRow()
            // console.log('first row:', row)3
 
            for(let cell = 0; cell < parseInt(col_num,10); cell++) {
            //  let y = x.insertCell(c);
                let cellEle = rowEle.insertCell(cell);
                cellEle.id = (`${row}-${cell}`)
                // console.log('row:', row)
                if(cell = namesArray.indexOf(namesArray[cell])) {
                    // sets class = name from names array in correct column 
                    // cellEle.className = namesArray[cell]
                    cellEle.className = `Player${cell}`
                    console.log('cell:', cell)
                    // ['ben', 'tom', 'chris']
                }
                // cellEle.className = 'data'
                // cellEle.contenteditable = 'true'
                cellEle.setAttribute('contenteditable', 'true')
            //   console.log(y.id)
                // cellEle.innerHTML="Row-"+row+" Column-"+cell;
                // console.log(cellEle)

                // I wonder if this is messing with the content editable being updated since I am adding a event listener of clikc on the element? 
                // cellEle.addEventListener("click", function(e) {
                //     console.log('add event listener is running')
                //     e.preventDefault();
                //     // id = this.id
                //     // sessionStorage.setItem('id', JSON.stringify(id));
                //     // console.log('id:', id)
                //     // row = id.substring(0, id.indexOf('-'))
                //     // console.log('id.indexOf('-'):', id.indexOf('-'))
                //     // console.log('typeof(id.indexOf('-')):', typeof(id.indexOf('-')))
                //     // this is returning the row not the col
                //     // console.log('row:', row)
                //     // idLastCharInd = (id.length - 1)

                //     // console.log('idLastCharInd:', idLastCharInd)
                //     // col = id.substring((id.indexOf('-') + 1))
                
                //     // col = id.substring(1, 3)
                //     // console.log('id.indexOf('-'):', id.indexOf('-'))
                //     // console.log('idLastCharInd:', idLastCharInd)
                //     // console.log('col:', col)

                //     // $(upDateScore(col, id))
                //     $(sumTotalTable)
                    
                // })

            //  make contenteditable true when other elements have contentiable filled out already. 

            // if the element clicked on is greater than or equal to row and col && all of those has inner.html != "" then do this....
                
                
            // id = JSON.parse(sessionStorage.getItem('id'))
            // console.log('this id is running:', id)

            // let col_num = id.substring((id.indexOf('-') + 1))

            // if(col_num = namesArray.length && )  

                $('[contenteditable="true"]').keypress(function(e) {
                    var x = event.charCode || event.keyCode;
                    // console.log('x:', x)
                    if (isNaN(String.fromCharCode(e.which)) && x!=46 || x===32 || x===13 || (x===46 && event.currentTarget.innerText.includes('.'))) e.preventDefault();
                    // console.log(currentTarget.id)

                
                
                // if document.getElementById(${`footer-${}`})
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
    // console.log('row:', row)
    }
}



// function upDateScore(col, id) {

//     // document.addEventListener("DOMContentLoaded") {
//     footer = document.getElementById(`foot-${col}`)
//     // console.log(footer)
//     // cellEle.addEventListener("click", function(e) {
//     //     console.log('add event listener is running')
//     //     e.preventDefault();
//     //     id = this.id)

//     if(footer.innerHTML = 'Score') {
//         // console.log('if statement is running in sum values')
//         cell = document.getElementById(id)
//         console.log('cell:', cell)
//         // console.log('cell.innerhtml:', cell.innerHTML)
//         // this is not actually getting the innnerHTML
//         // console.log(cell.innerText)
//         footer.innerHTML = `${cell.innerHTML}`
//         // document.getElementById(`foot-${col}`).innerHTML = `${cell.innerHTML}`
//         if(cell.innerHTML != '') {
//             console.log('this element has innerhtml')
//         //   inner html is not loading until second click on element
//         }
        

//         $(sumTotalTable)

//     } }
// }


function sumTotalTable() {
    // let rows = table.querySelectorAll('tr')
    let rows = $("#myTable").find("tbody>tr");
    // console.log("rows:", rows)

    // let footers = document.getElementsByClassName('footer')
    let footers = $(".footer")
    // console.log('footers:', footers)

    for (let i = 0; i < rows[0].cells.length; i++) {
        // console.log('rows[0].cells.length:', rows[0].cells.length)
        // console.log('note that these two should be equal')
        // console.log('namesArray.length:', namesArray.length)
        var sum = 0; 

        for (let j = 0; j < rows.length; j++) {
            console.log('rows.length:', rows.length)
            var cell = rows[j].cells[i];
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
            // sum += parseInt(cell.textContent, 10);
        }
        // innner loop you were not previously working with so that was your missing piece. 

        footers[i].textContent = sum;
    }

           // Add the sum cells to the new row
    //        for (let i = 0; i < footers.length; i++) {
    //         newRow.appendChild(sumCells[i]);

    // }

    $(declareWinOrLoss)
}

function declareWinOrLoss() {
    let userTotalObj = document.getElementById("foot-0")
    console.log("userTotalObj:", userTotalObj)
    // userTotal = userTotalObj.innerText
    let userTotalStr = userTotalObj.textContent
    let userTotal = parseInt(userTotalStr)

    let totalsObj = document.getElementsByClassName("footer")
  
    for(let i = 1; i < totalsObj.length; i++) {

        let total = parseInt(totalsObj[i].innerText, 10);
        console.log('total:', total)
        let input = document.getElementById('win')

        if(total >= userTotal) {
            console.log(false)
            let win = false
            input.setAttribute("value", `${win}`)
            // localStorage.setItem('win', win)
            }
        else {
            console.log(true)
            let win = true
            input.setAttribute("value", `${win}`)
        }
        // let input = document.getElementById('win')
        // console.log(input)
        // input.setAttribute("value", win)
       
    }
    // console.log(true)
    // let win = true

    // let num_players = namesArray.length
    // console.log("num_players:", num_players)
    // console.log("game_id:", game_id)
    // localStorage.setItem('win', win)
    // let input = document.getElementById('win')
    // console.log(input)
    // // input.setAttribute("value", win)
    // input.setAttribute("value", "true")
    // this works cant pass in win standby 
    // console.log(input)

    // $(generateButtonHTML(win, num_players, game_id))
    // $(createUploadForm(win, num_players))
    // const axios = require('axios')
    // const res = await axios.post('/log_play/${game_id}/save')
    // axios.post('/log_play/${game_id}/save', {
    //     Num_players: num_players, 
    //     Win: win
    //     .then(function (response) {
    //         console.log(response);
    //       })
    // })
    // saveResults(win, num_players)
}

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

    $(generateHeaderHTML)


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
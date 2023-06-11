

console.log('namesArray in score.js:', namesArray)



function generateGameHTML() {
    console.log('generateGameHTML is running in score.js')
    row_num = window.prompt("Input number of rows", 1);

    // console.log(namesArray)
    console.log(namesArray.length)
    col_num = namesArray.length;
    // console.log(cn)
    // console.log(players)
    // cn = window.prompt("Input number of columns",1);
      
     for(let r = 0; r < parseInt(row_num,10); r++) {
       let x=document.getElementById('myTable').insertRow(r);
       for(let c = 0; c < parseInt(col_num,10); c++) {
         let y = x.insertCell(c);
          y.id = (`${r}, ${c}`)
          console.log(y.id)

          y.innerHTML="Row-"+r+" Column-"+c; 


        if (y.id[0] == 0) {
            // console.log(y.id[0][1])
            console.log('if statement is running')
            
            for(i = 0; i <namesArray.length; i++) {
            console.log('for statement is running')
        //     console.log('namesArray.length:', namesArray.length)
                console.log('i:', i)
                console.log('namesArray[i]:', namesArray[i])
                let id = (`0, ${i}`)
                // my understanding of this is that i should be equal to 0, 1, and 2 becuase of the for loop 
                // i = 0 (i starts at zero) i < namesArray.length if names array.length = 3 (i will stop at 2)
                // i++ (i will continue in incriments of one)
                // this should give me three ids 
                console.log(id)

                document.getElementById(id).innerHTML = namesArray[i]
                // this is getting the element by id (three ids) and should be setting the value as the value of namesArray index of i 
            }
              }

        // y.innerHTML="Row-"+r+" Column-"+c; 
            // y.innerHTML = y.id
        }
     }

 }
 $(generateGameHTML);



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
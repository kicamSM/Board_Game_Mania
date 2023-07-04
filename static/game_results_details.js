

function generateMatchHTML(num_players, matchId, matchData, timeStamp) {
  console.log('matchData', matchData)

  // let email;
  // let score;
  // let win;
  let noSpaceEmails = []
  let noSpaceScores = []
  let noSpaceWins = []

  for(let i = 0; i < matchData.length; i++) {
    console.log('md.len', matchData.length)
    let email = matchData[i].email
    // console.log('email', email)
    let score = matchData[i].score
    let win = matchData[i].win
    // console.log('matchData', matchData[0])
    // for (let j = 0; j < matchData.length; j++) {
      
      // console.log('this for loop is running')
      noSpaceEmails.push(matchData[i].email)
      noSpaceScores.push(matchData[i].score)
      noSpaceWins.push(matchData[i].win)
      // console.log('matchData[i][j]', matchData[i][j])
    }
    // console.log('detailsArray', detailsArray)
    // console.log('emails', emails)
    // console.log('scores', scores)
    // console.log('wins', wins)
    let emails = noSpaceEmails.map((item) => ` ${item}`)
    let scores = noSpaceScores.map((item) => ` ${item}`)
    let wins = noSpaceWins.map((item) => ` ${item}`)
  
    
    // let html = `<li class="info"> Email: ${email} </li>
    // <li class="info"> Score: ${score} </li>
    // <li class="info"> Win: ${win} </li>`
    // document.createElement('ul')
    // document.getElementById('match_ul').append(html)

    // {{% for playerData in matchData %}}
    //         <li class="info"> Email: ${playerData.email} </li>
    //         <li class="info"> Score: ${playerData.score} </li>
    //         <li class="info"> Win: ${playerData.win} </li>
    //         {{% endfo3
    // r %}}

    // }
    return `
    <div class="card p-4" style="width: 800px" id="${matchId}">
      <div class="text-center" id="match-details"> 
        <div>
          <h3 class="card-title">Date Match Was Played: ${timeStamp}</h3>
          <h2 class="card-title"></h2>
        </div>
          <div>
            <ul id="match-ul">
              <li class="info"><font size="+1"><b>Number of Players:</b> ${num_players}</font></li>
              <li class="info"><font size="+1"><b>Players Emails:</b> ${emails}</font></li>
              <li class="info"><font size="+1"><b>Players Scores:</b> ${scores}</font></li>
              <li class="info"><font size="+1"><b>Players Wins:</b> ${wins}</font></li>
            </ul>
          </div>
        </div>
      </div>
    `;

    
  // }
}
function generateMatchDetailsHTML(matchData) {
    console.log('matchData in generateMatchDetailsHTML', matchData)
    let email;
    let score;
    let win;
    for(let i = 0; i < matchData.length; i++) {
      console.log('md.len', matchData.length)
      email = matchData[i].email
      // console.log('email', email)
      score = matchData[i].score
      win = matchData[i].win

      }

      let html = ` <li class="info"> Email: ${email} </li> 
              <li class="info"> Score: ${score} </li>
              <li class="info"> Win: ${win} </li>`

      // $("#match-ul").append(html);
      // document.getElementById('match-ul').append(html)
            
    }
  // console.log('curmtch', currentMatch)
  // return ` <li class="info"> ${currentMatch} </li>`
  // }

async function getMatchInformation() {
  // const dateTimes = [];


    // for(const timeStamp of timeStamps) {
    //   let dateTime = new Date(timeStamp);
    //   // const date = dateTime.date.split(" ")[0];
  
    //   console.log('dateTime', dateTime)
    //   console.log('typeof(dateTime)', typeof(dateTime))
    //   console.log('dt', dateTime.date)
    //   dateTimes.push(dateTime);
    // }
    // console.log('dt', dateTimes)


    for(let i = 0; i < matchIdList.length; i++) {
      let thisMatchData = []

      for(let j = 0; j < matchDataList.length; j++) {
      // console.log('this is how many times this is running!!!')
        if (matchDataList[j]['match_id'] === Number(matchIdList[i])) {
          thisMatchData.push(matchDataList[j])
      }
    }
    // console.log('timstamps', timeStamps)
      // console.log('these matches', these_matches)
    let newMatch = $(generateMatchHTML(thisMatchData.length, matchIdList[i], thisMatchData, timeStamps[i]))
    // need to get out every dict in list where the matchDataList match_id = matchIdList[i]
    // let newMatchDetails = $(generateMatchDetailsHTML(thisMatchData))
    // console.log(matchIdList)
    $("#match-details").append(newMatch);
    // $("#match-ul").append(newMatchDetails);
    }
}
$(getMatchInformation);

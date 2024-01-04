let mock_player_list = [

  {
    playerName: "Chose",
    img: "<magnifique lien d'image profile2>",
  },
  {
    playerName: "Binouche",
    img: "<magnifique lien d'image profile2>",
  },
];


const default_lobby_template = document.getElementById('lobby').innerHTML;
// console.log(default_lobby_template)


let reset_default_lobby = function () {
  document.getElementById('lobby').innerHTML = default_lobby_template;
}

let hide_excess_player_profiles = function (nb_rackets) {
  // currentGameType.racketCount
  console.log("hide_excess_player_profiles :: nb_rackets : " + nb_rackets);

  for (let i=0; i < 4; i++) {
    // lobbyProfile1
    profElemID = `lobbyProfile${i + 1}`;
    profElem = document.getElementById(profElemID);
    if (i < nb_rackets)
      profElem.style.display = 'flex';
    else
      profElem.style.display = 'none';
  }
}

let update_local_1p_info = function (player_info) {

  console.log("update_local_2p_info info CALLED.");
  document.getElementById("imgPlayer1").src = player_info.img;
  document.getElementById("namePlayer1").innerHTML = player_info.login;
  // document.getElementById("imgPlayer2").src = img;
  document.getElementById("imgPlayer2").style.border = "3px outset #34eb34";
  document.getElementById("namePlayer2").innerHTML = "Celine Incognito";
}

let update_local_2p_info = function (player_info) {

  console.log("update_local_2p_info info CALLED.");
  document.getElementById("imgPlayer1").src = player_info.img;
  document.getElementById("namePlayer1").innerHTML = player_info.login;
  // document.getElementById("imgPlayer2").src = img;
  document.getElementById("imgPlayer2").style.border = "3px outset #34eb34";
  document.getElementById("namePlayer2").innerHTML = "Guest";
}


let update_player_info = function (player_info_list) {

  console.log('update_player_info CALLED : ' + player_info_list);
  document.getElementById("startEngine").disabled = false;
  reset_default_lobby()
  if (isTournament && !isTournamentStage1 && !isTournamentStage2)
    hide_excess_player_profiles(4);
  else
    hide_excess_player_profiles(currentGameInfo.racketCount);

  console.log('currentGameType : ' + currentGameType)
  if (currentGameType === 'Local_1p')
    update_local_1p_info(player_info_list[0]);
  else if (currentGameType === 'Local_2p')
    update_local_2p_info(player_info_list[0]);

  else {
    console.log("update_player_info info CALLED.");
    let i = 0;
    for (ply of player_info_list) {
      imgElemID = `imgPlayer${++i}`;
      nameElemID = `namePlayer${i}`;
      login = ply.login;
      img = ply.img;
      ready = ply.ready;

      // if (isTournament)
      // {
      //   if (player_info_list[0])
      //   {
      //     player1Login = player_info_list[0].login;
      //     document.getElementById('nameP1').innerHTML = ` ${'player1Login'}`;
      //   }
      //   if (player_info_list[1])
      //   {
      //     player2Login = player_info_list[1].login;
      //     document.getElementById('nameP2').innerHTML = ` ${'player2Login'}`;
      //   }
      //   if (player_info_list[2])
      //   {
      //     player3Login = player_info_list[2].login;
      //     document.getElementById('nameP3').innerHTML = ` ${'player3Login'}`;
      //   }
      //   if (player_info_list[3])
      //   {
      //     player4Login = player_info_list[3].login;
      //     document.getElementById('nameP4').innerHTML = ` ${'player4Login'}`;
      //   }

      //   if (isGhostLobby)
      //   {
      //     player1Score1 = player_info_list[0].score;
      //     player1Score2 = player_info_list[0].score;
      //     player2Score1 = player_info_list[1].score;
      //     player2Score2 = player_info_list[1].score;
      //     player3Score1 = player_info_list[2].score;
      //     player3Score2 = player_info_list[2].score;
      //     player4Score1 = player_info_list[3].score;
      //     player4Score2 = player_info_list[3].score;

      //     if (player_info_list[0].score > player_info_list[1].score) {
      //       document.getElementById('nameWinner1').innerHTML = `${'player1Login'}`;
      //     }
      //     else {
      //       document.getElementById('nameWinner1').innerHTML = `${'player2Login'}`;
      //     }

      //     if (player_info_list[2].score > player_info_list[3].score) {
      //       document.getElementById('nameWinner2').innerHTML = `${'player2Login'}`;
      //     }
      //     else
      //       document.getElementById('nameWinner2').innerHTML = ` $player3Login`;

      //     document.getElementById('scoreP1').innerHTML = ` ${'player1Score1'}`;
      //     document.getElementById('scoreP2').innerHTML = ` ${'player2Score1'}`;
      //     document.getElementById('scoreP3').innerHTML = ` ${'player3Score1'}`;
      //     document.getElementById('scoreP4').innerHTML = ` ${'player4Score1'}`;
      //   }
      // }
      // if (isGhostLobby)
      // {
      //   // //Score of ply.login at tourn1ElemID
      //   // document.getElementById('scoreP1').innerHTML = ` ${score}`;
      //   // //Score of ply.login at tourn1ElemID
      //   // document.getElementById('scoreP2').innerHTML = ` ${score}`;
      //   // //Score of ply.login at tourn1ElemID
      //   // document.getElementById('scoreP3').innerHTML = ` ${score}`;
      //   // //Score of ply.login at tourn1ElemID
      //   // document.getElementById('scoreP4').innerHTML = ` ${score}`;

        //Row 2 Match
      // if (isGhostLobby)
      //   document.getElementById(tourn2ElemID).innerHTML =  `${login}`;
        // isTournament = False;
      // }
      document.getElementById(imgElemID).src = img;
      document.getElementById(nameElemID).innerHTML = ` ${login}`;
      if (ready)
      {
        console.log(`Player ${i} is ready`);
        // document.getElementById(imgElemID).style.border = "3px outset #34eb34";
        document.getElementById(imgElemID).style.border = "3px outset " + playerColors[i];
      }
    }
  }
}

let on_click_update_players = function () {
  update_player_info(mock_player_list);
};

//Signal that send to the server that this player is ready to join the game.
let signal_player_ready = function() {
  document.getElementById("startEngine").disabled = true;
  document.getElementById("startEngine").innerHTML = "READY!";
  document.getElementById("custom-spinner").style.display = "block";
  let payload = {
    'ev': 'ready'
  }
  console.log('Sending payload : ' + payload);
  gameWebSock.send(JSON.stringify(payload));
  console.log('Payload sent.');
}

let reset_endgame_messages = function () {
  document.getElementById("winnerMsg").innerHTML = "WINNER !";
  document.getElementById("winner").style.display = "none";
  document.getElementById("loser").style.display = "none";
  document.getElementById("crash").style.display = "none";
  document.getElementById("finish").style.display = "none";
  document.getElementById("wallofshame").style.display = "none";
  document.getElementById("buttonGhostLobby").style.display = "none";
}

let find_quitter_info = function (playerInfo, quitterID) {
  for (const [key, value] of Object.entries(playerInfo)) {
    console.log('find_quitter_info :: key ' + key);
    console.log('find_quitter_info :: value ' + value);
    console.log('find_quitter_info :: value.name ' + value.name);
    if (value.playerID == quitterID)
      return value;
  }
  return undefined;
}

let loadEndGame = function (data) {
  console.log('end is: ' + data.endState);
  console.log('loadEndGame :: data : ' + data)
  console.log('loadEndGame :: data.playerInfo : ' + data.playerInfo)
  console.log('-=-= loadEndGame :: data.winingTeam : ' + data.winingTeam);
  reset_endgame_messages();
  loadModule('aftergame');

  console.log(" data.playerInfo : " +  data.playerInfo)
  console.log("isTournament : " + isTournament)
  // document.getElementById("buttonGhostLobby").style.display = "none";

  if (data.endState === 'quit'){
    console.log('***wallOfShame');
    console.log("winnerID : " + data.winingTeam);
    console.log("quitterID : " + data.quitter);
    let quitterID = data.quitter;
    let quitter_info = find_quitter_info(data.playerInfo, quitterID);
    console.log("quitter_info : " + quitter_info);
    let quitter_name = quitter_info.name;
    let quitter_img = data.wallofshame;
    console.log("loadEndGame :: quitterIMG : " + quitter_img);
    console.log("loadEndGame :: shameVictim : " + quitter_name);

    document.getElementById("wallofshame").style.display = "block";
    document.getElementById("quiiterIMG").src = quitter_img;
    document.getElementById("shameVictim").innerHTML = quitter_name;
  }
  else if (data.endState === 'abort'){
    console.log('*****crash');
    document.getElementById("crash").style.display = "block";
  }
  else if (currentGameType === 'Local_1p' || currentGameType === 'Local_2p' ) {
    console.log('LOCAL GAME');
    document.getElementById("finish").style.display = "block";
  }
  else if (data.endState === 'win') {
    let winnerID = data.winingTeam;
    let winner = data.playerInfo[winnerID];
    let user_is_winner = (parseInt(winner.playerID) == user_id);

    console.log("winnerID : " + winnerID)
    console.log("winner : " + winner)
    console.log("user_is_winner : " + user_is_winner)

    if (user_is_winner) {
      console.log('**win');
      document.getElementById("winner").style.display = "block";
      if (isTournament) {// && !isTournamentStage2){
        if (isTournamentStage2) {
          console.log('** win - next game');
          document.getElementById("winnerMsg").innerHTML = "YOU WON THE TOURNAMENT !!!";
        } else {
          // document.getElementById("winnerMsg").innerHTML = "WINNER !";
          document.getElementById("buttonGhostLobby").style.display = "block";
        }
      }
    }
    else {
      console.log('***lose', namePlayer1);
      document.getElementById("loser").style.display = "block";
    }
  }
  // else {
  //   if (currentGameType === 'Local_1p' || currentGameType === 'Local_2p' ) {
  //     console.log('LOCAL GAME');
  //     document.getElementById("finish").style.display = "block";
  //   }
  //   else {
  //     console.log('***lose', namePlayer1);
  //     document.getElementById("loser").style.display = "block";
  //   }
  // }
  // else if (data.endState !== 'crash' && (currentGameType === 'Local_1p' || currentGameType === 'Local_2p' ) ){
  //   console.log('LOCAL GAME');
  //   document.getElementById("finish").style.display = "block";
  // }
  // else if (data.endState !== 'crash'){
  //   console.log('***lose', namePlayer1);
  //   document.getElementById("loser").style.display = "block";
  // }

  // disconnect_socket();
}

let loadTournamentQuitterEnding = function (quitterData) {
  console.log('QuitterData received : ' + quitterData);
  reset_endgame_messages();
  loadModule('aftergame');

  let quitter_name = quitterData.name;
  let quitter_img = quitterData.img;
  document.getElementById("wallofshame").style.display = "block";
  document.getElementById("quiiterIMG").src = quitter_img;
  document.getElementById("shameVictim").innerHTML = quitter_name;

  console.log('Disconnecting game socket and tournament socket ...');
  disconnect_socket();
  disconnect_tour_socket();
  console.log('All sockets closed !');
}



let signal_final_game = function() {
  console.log('signal_final_game :: entered !')
  console.log('signal_final_game :: tourWebSock :' + tourWebSock)

  if (tourWebSock == null) {
    console.error('Trying to signale join final game while no tournament socket exists.')
    disconnect_socket();
    disconnect_tour_socket();
    return;
  }
  let payload = JSON.stringify({
    'ev': 'final'
  });
  // console.log('Sending payload : ' + payload);
  // gameWebSock.send(JSON.stringify(payload));
  // console.log('Payload sent.');
  console.log('load final game.');
  loadModule('lobby');
  tourWebSock.send(payload);
  // document.getElementById("loser").style.display = "block";

}

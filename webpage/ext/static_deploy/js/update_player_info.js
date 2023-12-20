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

  if (isTournament)
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
      tourn1ElemID = `nameP${i}`;
      tourn2ElemID = `nameWinner${i}`;
      // scoreP1 = `ply.score${nameElemID}`;
      // scoreP2 = `ply.score${nameElemID}`;
      // scoreP3 = `ply.score${nameElemID}`;
      // scoreP4 = `ply.score${nameElemID}`;
      login = ply.login;
      img = ply.img;
      ready = ply.ready;
      score  = ply.score;

      // console.log('login : ' + login)
      // console.log('img : ' + img)
      // console.log('ready : ' + ready)
      if (isTournament)
      {
        document.getElementById(tourn1ElemID).innerHTML = ` ${login}`;
      }
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

      //   //Row 2 Match
      //   document.getElementById(tourn2ElemID).innerHTML =  `${login}`;
      //   isTournament = False;
      // }
      document.getElementById(imgElemID).src = img;
      document.getElementById(nameElemID).innerHTML = ` ${login}`;
      if (ready)
      {
        console.log(`Player ${i} is ready`);
        document.getElementById(imgElemID).style.border = "3px outset #34eb34";
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
  document.getElementById("winner").style.display = "none";
  document.getElementById("loser").style.display = "none";
  document.getElementById("crash").style.display = "none";
  document.getElementById("finish").style.display = "none";
}

let loadEndGame = function (data) {
  console.log('end is: ' + data.endState);
  console.log('loadEndGame :: data : ' + data)
  console.log('loadEndGame :: data.playerInfo : ' + data.playerInfo)
  console.log('-=-= loadEndGame :: data.winingTeam : ' + data.winingTeam);
  reset_endgame_messages();
  loadModule('aftergame');

  let winnerID = data.winingTeam;

  let winner = data.playerInfo[winnerID];
  let user_is_winner = (winner.playerID == user_id);

  console.log(" data.playerInfo : " +  data.playerInfo)
  console.log("winnerID : " + winnerID)
  console.log("winner : " + winner)
  console.log("user_is_winner : " + user_is_winner)

  if (data.endState === 'crash' || winnerID == undefined){
    console.log('*****crash');
    document.getElementById("crash").style.display = "block";
  }
  else if (user_is_winner ) {
    console.log('**win');
    document.getElementById("winner").style.display = "block";
    if (isTournament){
      console.log('** win - next game');
      document.getElementById("gameButtonA").style.display = "block";
    }

  }
  else if (data.endState !== 'crash' && (currentGameType === 'Local_1p' || currentGameType === 'Local_2p' ) ){
    console.log('LOCAL GAME');
    document.getElementById("finish").style.display = "block";
  }
  else if (data.endState !== 'crash'){
    console.log('***lose', namePlayer1);
    document.getElementById("loser").style.display = "block";
  }
  disconnect_socket();
}

let signal_final_game = function() {
  // let payload = {
  //   'ev': 'final'
  // }
  // console.log('Sending payload : ' + payload);
  // gameWebSock.send(JSON.stringify(payload));
  // console.log('Payload sent.');
  console.log('load final game.');
}



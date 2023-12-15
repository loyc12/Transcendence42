let mock_player_list = [
  //  {
  //    playerName: "Jambon",
  //    img: "<magnifique lien d'image profile1>",
  //  },
  //  {
  //    playerName: "Pepperoni",
  //    img: "<magnifique lien d'image profile2>",
  //  },
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
console.log(default_lobby_template)


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

      console.log('login : ' + login)
      console.log('img : ' + img)
      console.log('ready : ' + ready)

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
  //document.getElementById("custom-spinner").style.alignItems = "center";
  document.getElementById("custom-spinner").style.display = "block";
  let payload = {
    'ev': 'ready'
  }
  console.log('Sending payload : ' + payload);
  gameWebSock.send(JSON.stringify(payload));
  console.log('Payload sent.');

  /// DEBUG
  // loadModule('game');

  /// GREY out button
}

let loadEndGame = function (data) {
  // console.log('end is: ' + getEndInfo().endState);
  console.log('=== CALLED loadEndGame STATE:' + data.endState );
  if (data.endState === 'win'){
    console.log('**win');
    document.getElementById("winner").style.display = "block";
    document.getElementById("crash").style.display = "none";
    loadModule('aftergame');
  }
  else if (data.endState !== 'crash'){
    console.log('***lose');
    document.getElementById("loser").style.display = "block";
    document.getElementById("crash").style.display = "none";
    loadModule('aftergame');
  }
  else if (data.endState === 'crash'){
    console.log('*****crash');
    loadModule('aftergame');
  }
  disconnect_socket();
}

// { // getEndInfo()
//   "gameType": "pong", //  random == doesn't matter( create random one if none are joinable )
//   "gameMode": "solo", //  solo, dual, freeplay, tournament
//   "endState": "win", //   win, quit, crash
//   "winingTeam": 1, //     teamID
//   "quitter": 2, //        playerID
//   "scores": [
//       "s1",
//       "s2",
//       "s3",
//       "s4"
//   ],
//   "playerInfo": getPlayerInfo{}
// }
















const default_lobby_template = document.getElementById('lobby').innerHTML;

let reset_default_lobby = function () {
  document.getElementById('lobby').innerHTML = default_lobby_template;
}

let hide_excess_player_profiles = function (nb_rackets) {
  for (let i=0; i < 4; i++) {
    profElemID = `lobbyProfile${i + 1}`;
    profElem = document.getElementById(profElemID);
    if (i < nb_rackets)
      profElem.style.display = 'flex';
    else
      profElem.style.display = 'none';
  }
}

let update_local_1p_info = function (player_info) {
  document.getElementById("imgPlayer1").src = player_info.img;
  document.getElementById("namePlayer1").innerHTML = player_info.login;
  document.getElementById("imgPlayer2").style.border = "3px outset #34eb34";
  document.getElementById("namePlayer2").innerHTML = "Celine Incognito";
}

let update_local_2p_info = function (player_info) {
  document.getElementById("imgPlayer1").src = player_info.img;
  document.getElementById("namePlayer1").innerHTML = player_info.login;
  document.getElementById("imgPlayer2").style.border = "3px outset #34eb34";
  document.getElementById("namePlayer2").innerHTML = "Guest";
}


let update_player_info = function (player_info_list) {
  document.getElementById("startEngine").disabled = false;
  reset_default_lobby()
  if (isTournament)
    hide_excess_player_profiles(4);
  else
    hide_excess_player_profiles(currentGameInfo.racketCount);

  if (currentGameType === 'Local_1p')
    update_local_1p_info(player_info_list[0]);
  else if (currentGameType === 'Local_2p')
    update_local_2p_info(player_info_list[0]);

  else {
    let i = 0;
    for (ply of player_info_list) {
      imgElemID = `imgPlayer${++i}`;
      nameElemID = `namePlayer${i}`;
      login = ply.login;
      img = ply.img;
      ready = ply.ready;

      // if (isGhostLobby)
      //   document.getElementById(tourn2ElemID).innerHTML =  `${login}`;
      document.getElementById(imgElemID).src = img;
      document.getElementById(nameElemID).innerHTML = ` ${login}`;
      if (ready)
      {
        document.getElementById(imgElemID).style.border = "3px outset #34eb34";
      }
    }
  }
};

let on_click_update_players = function () {
  update_player_info(mock_player_list);
};

let signal_player_ready = function() {
  document.getElementById("startEngine").disabled = true;
  document.getElementById("startEngine").innerHTML = "READY!";
  document.getElementById("custom-spinner").style.display = "block";
  let payload = {
    'ev': 'ready'
  }
  gameWebSock.send(JSON.stringify(payload));
}

let reset_endgame_messages = function () {
  document.getElementById("winner").style.display = "none";
  document.getElementById("loser").style.display = "none";
  document.getElementById("crash").style.display = "none";
  document.getElementById("finish").style.display = "none";
}

let loadEndGame = function (data) {
  reset_endgame_messages();
  loadModule('aftergame');

  let winnerID = data.winingTeam;
  let winner = data.playerInfo[winnerID];
  let user_is_winner = (parseInt(winner.playerID) == user_id);

  document.getElementById("buttonGhostLobby").style.display = "none";

  if (data.endState === 'crash' || winnerID == undefined){
    document.getElementById("crash").style.display = "block";
  }
  else if (data.currentGameType === 'Local_1p' || data.currentGameType === 'Local_2p' ) { 
    document.getElementById("finish").style.display = "block";
  }
  else if (user_is_winner ) {
    document.getElementById("winner").style.display = "block";
    if (isTournament){
      document.getElementById("buttonGhostLobby").style.display = "block";
    }
  }
  else if (data.endState !== 'crash'){
    document.getElementById("loser").style.display = "block";
  }
  else if (data.endState === 'wallOfShame'){
    document.getElementById("wallofshame").style.display = "block";
  }
};

let signal_final_game = function() {
  if (tourWebSock == null) {
    disconnect_socket();
    disconnect_tour_socket();
    return;
  }
  let payload = JSON.stringify({
    'ev': 'final'
  });
  loadModule('lobby');
  tourWebSock.send(payload);
};

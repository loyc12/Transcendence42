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

let update_player_info = function (player_info_list) {
  elems = [];
  elems.push(document.getElementById("player1"));
  elems.push(document.getElementById("player2"));
  elems.push(document.getElementById("player3"));
  elems.push(document.getElementById("player4"));

  player_info_list;
  for (let i = 0; i < elems.length; i++) {
    elems[i].textContent = player_info_list[i]["playerName"];
  }
};

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

let loadEndGame = function () {
  loadModule('afterGame');
  disconnect_socket()
}
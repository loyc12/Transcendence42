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

  console.log('update_player_info CALLED : ' + player_info_list);


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

    //img_elem = document.getElementById(imgElemID);
    // document.getElementById(imgElemID) = login;
    document.getElementById(imgElemID).src = img;
    document.getElementById(nameElemID).innerHTML = `Player ${i} : ${login}`;
    if (ready)
      document.getElementById(imgElemID).style.borderBlockColor = "green";

    // img_elem.src = img;
    // name_elem.innerHTML = `Player ${i} : ${login}`;
  }
  // for (ply of players) {
  //   imgElemID = ``
  // }

  // profil_elem = document.getElementById("lobbyProfile1");
  // img_elem1 = document.getElementById("imgPlayer1");
  // img_elem2 = document.getElementById("imgPlayer2");
  // // img_elem3 = document.getElementById("imgPlayer3");
  // img_elem4 = document.getElementById("imgPlayer4");
  // // img_elem1.src = '';
  // // img_elem2.src =
  // // img_elem3.src =
  // // img_elem4.src =

  // // name_elem1 = document.getElementById("namePlayer1");
  // // name_elem2 = document.getElementById("namePlayer2")
  // // name_elem3 = document.getElementById("namePlayer3")
  // name_elem4 = document.getElementById("namePlayer4")
  // player_name = 'Bobby !';
  // name_elem4.innerHTML = `Player4 : ${player_name}`;////'<div class="align-right4 style="color: #f0ffff; font-size: 40px;" id="namePlayer1">Player1 : Bobby ! </div>';
  // //name_eme2.innerHTML= "Player1 :" + {{ namePlayer1 }}




  // elems = [];
  // elems.push(document.getElementById("lobbyProfil_img1"));
  // elems.push(document.getElementById("player2"));
  // elems.push(document.getElementById("player3"));
  // elems.push(document.getElementById("player4"));

  // player_info_list;
  // for (let i = 0; i < elems.length; i++) {
  //   elems[i].textContent = player_info_list[i]["playerName"];
  // }
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
  disconnect_socket();
}
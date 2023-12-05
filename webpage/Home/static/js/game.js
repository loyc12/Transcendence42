//COLLE
function myFunction() {
    alert("Hello from a static file!");
}

let _build_join_request_payload = function (gameMode, gameType, withAI=false, eventID=0) {
  return {
      'gameMode': gameMode,
      'gameType': gameType,
      'withAI': withAI,
      'eventID': eventID
  }
}

let _http_join_request = function (payload) {

  let gameID = null;

  fetch('https://' + window.location.host + '/game/join/', {
      method: "POST",
      body: JSON.stringify(payload),
      credentials: 'same-origin',
      headers: {
          "X-CSRFToken": getCookie("csrftoken")
      }
  })
  .then (function(data) {
      console.log('Returned data from game join request : ' + data)
      if (data.has('gameID'))
          gameID = data['gameID']
  })
  .catch(err => console.log(err));

  return gameID;
}

let request_join_game = function (gameType) {
  
  console.log('request_join_game temporarly deactivated. Come back again later.')
  //return ;
  if (gameType === 'Local_1p') {
    payload = _build_join_request_payload('Local_1p', 'Ping', true);
  } else if (gameType === 'Local_2p') {
    payload = _build_join_request_payload('Local_2p', 'Pong', false);
  } else if (gameType === 'Tournament') {
    payload = _build_join_request_payload('Tournament', 'Pong', false);
  } else if (gameType === 'Multiplayer') {
    payload = _build_join_request_payload('Multiplayer', 'Ping', false);
  } else if (gameType === 'Online_4p') {
    payload = _build_join_request_payload('Online_4p', 'Pingest', false);
  } else {
    throw TypeError('Trying to request join game with unimplemented gameType: ' + gameType)
  }

  const gameID = _http_join_request(payload)

  console.log('gameID at request_join_game() end : ' + gameID)
  return gameID;
}

let send_ready_signal = function () {
  /// Called when player is connected to websocket and wants to set themself as ready to start playing.

  fetch('https://' + window.location.host + '/game/ready/', {
      method: "POST",
      credentials: 'same-origin',
      headers: {
          "X-CSRFToken": getCookie("csrftoken")
      }
  })
  .then (function(data) {
      console.log('Ready signal was received and handled SUCCESSFULLY')
  })
  .catch(err => console.log(err));
}

/*
let join_payload_builder = function (gameMode, gameType, withAI, eventID=0) {

}

let request_join_game = function (gameType) {
  console.log('request game join with gametype : ' + gameType)

  switch (gameType) {

    case 'Tournament':
      break;
    case 'Multiplayer':
      break;
    case 'Local_1p':
      break;
    case 'Local_2p':
      break;
    default:
      throw TypeError('Trying to request join game with bad gameType. ')
  }
}
*/

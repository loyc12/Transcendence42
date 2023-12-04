function myFunction() {
    alert("Hello from a static file!");
}

function getCookie(name) {
  console.log('document.cookie : ' + document.cookie)
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

let _build_join_request_payload = function (gameMode, gameType, withAI=false, eventID=0) {
  return {
      'gameMode': gameMode,
      'gameType': gameType,
      'withAI': withAI,
      'eventID': eventID
  }
}

let _http_join_request = async function (payload) {

  console.log('request join game path : ' + 'https://' + window.location.host + '/game/join/')
  //const csrftoken = getCookie('csrftoken')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  console.log('csrftoken : ' + csrftoken)
  console.log('csrf from query selector : ' + document.querySelector('[name=csrfmiddlewaretoken]').value);
  
  return fetch('http://' + window.location.host + '/game/join/', {
      method: "POST",
      body: JSON.stringify(payload),
      credentials: 'same-origin',
      headers: {
          "X-CSRFToken": csrftoken
      }
  })
  .then (function(response) {
    return response.json()
  })
  .then (function(data) {
    if (data.status === 'failure')
      alert('Join game request failed because : \n\t - ' + data.reason)
      //throw new reportError('Join game request failed because : ' + data.reason)
    if (data.sockID) {
      console.log('Returned data from game join request : ' + data);
      console.log('response status : ', data.status);
      console.log('response reason : ', data.reason);
      console.log('response sockID : ', data.sockID);
      console.log('response gameType : ', data.gameType);
      console.log('response gameMode : ', data.gameMode);
      console.log('response withAI : ', data.withAI);
      console.log('response eventID : ', data.eventID);
      //if (data.has('sockID'))
      return data.sockID;
    }
  })
  //.catch(err => console.log(err));
}

let request_join_game = async function (gameType) {
  
  //console.log('request_join_game temporarly deactivated. Come back again later.')
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

  const sockID = await _http_join_request(payload)

  //console.log('sockID at request_join_game() end : ' + sockID)
  return sockID;
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

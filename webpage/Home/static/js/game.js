
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

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  return fetch('https://' + window.location.host + '/game/join/', {
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
    if (data.status === 'failure') {
      throw new reportError('Join game request failed because : ' + data.reason)
    }
    if (data.sockID) {
      return data;
    }
  })
  .catch(err => console.log(err));
}

let request_join_game = async function (gameType) {

  currentGameType = gameType
  if (gameType === 'Local_1p') {
    payload = _build_join_request_payload('Local_1p', 'Pong', true);
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

  gameData = await _http_join_request(payload)

  return gameData;
}

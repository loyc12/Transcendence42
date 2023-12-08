
let gameID;
let webSockPath;
let webSock;


// keyboard keys
let UP =     'up';
let DOWN =   'dn';
let LEFT =   'lf';
let RIGHT =  'rt';
let SPACE =  ' ';

// keypad keys
let KW = 'w';
let KS = 's';
let KA = 'a';
let KD = 'd';
let NZERO = '0';

let START = 'start_game';
let CLOSE = 'end_game';
let KEYPRESS = 'key_press';
let ESCAPE = None;
let RETURN = None;


let _send_player_keyevent = function(key) {
    payload = JSON.stringify({
        'ev': KEYPRESS,
        'key': key
    })
    webSock.send(payload)
}


let _get_websocket_path = function(gameID) {
    return 'ws://' + window.location.host + '/game/ws/' + gameID + '/';
}

let _on_game_event = function(event) {
    const data = JSON.parse(event.data);
    console.log('ev : ' + data.ev)
    if (data.ev === 'up') {
        console.log('UPDATE event received from websocket.');
        console.log(data)
        //...
    }
    else if (data.ev === "players") {
        console.log('PLAYERS event received from websocket.');
        console.log(data)
        //...
    }
    //else {
    //   document.querySelector('#ws_init_msg').innerHTML = data.msg;
    //}
}

let _on_server_side_disconnect = function(e) {
    console.error('The server disconnecter you');
};

let _connect_to_game_socket = function (webSockPath) {
    let sock;

    try {
        sock = new WebSocket(webSockPath);
    } catch (err) {
        alert('Failed To connect to server websocket.')
    }
    return sock;
}


let _prepare_websocket = function (webSock) {
    webSock.onmessage = _on_game_event;
    webSock.onmessage = _on_server_side_disconnect;
    //... Might be more initialisation latter ...
}

let loadMegaModule = function (gameType) {
    
    console.log('LOAD MEGA MODULE STARTING GAME JOIN PROCESS !')
    // Send HTTP POST request to get matched to a game in the MatchMaker or create a new one
    gameID = request_join_game(gameType);
    return;
    webSockPath = _get_websocket_path(gameID);
    webSock = _connect_to_game_socket(webSockPath)
    _prepare_websocket(webSock);
    
    // TODO: Enable Start/Ready button click
    // ...
}
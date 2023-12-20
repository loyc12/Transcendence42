
let tourWebSockID = null;
let tourWebSock = null;

let _on_tour_event = function(event) {
    console.log('User received event from tournament websocket');
    const data = JSON.parse(event.data);

    if (data.ev === 'connect') {
        console.log('User received message from server after tournament websocket connection : ' + data.msg);
    }
    else if (data.ev === 'game_connect') {
        console.log('Client Received Game connection order from tournament socket')
        console.log('Game connect order received data : ' + data)
        reset_default_lobby();
        gameType = data.form.gameMode;
        console.log('_on_tour_event :: data.form : ' + data.form)
        console.log('_on_tour_event :: gameType received from data.form.gameType : ' + gameType)
        parseInitData(get_default_init_state(gameType));

        disconnect_socket()
        gameSockID = data.sockID;
        gameEventID = data.form.eventID;
        gameWebSockPath = _get_websocket_path();
        gameWebSock = _connect_to_game_socket(gameWebSockPath);
        _prepare_websocket(gameWebSock);
    }
    else if (data.ev === 'brackets') {
        console.log('WoOoW ! received tournament brackets info : ' + data.brackets)
    }
}

// let _build_tour_ws_path = function(sockID) {
function _build_tour_ws_path(sockID) {
    return 'wss://' + window.location.host + '/tournament/ws/' + sockID + '/';
}

let _connect_to_tour_socket = function (tourWebSockPath) {
    let sock;

    console.log('Connecting to USER websocket at : ', tourWebSockPath)
    try {
        sock = new WebSocket(tourWebSockPath);
    } catch (err) {
        alert('Failed To connect to server TOURNAMENT websocket.')
    }
    return sock;
}


let _on_server_side_tour_disconnect = function(e) {
    console.error('The server disconnecter tournament');
    console.log('Server closed tournament websocket connection. Current socket readyState : ');
    // user_id = null;
};

let _prepare_tour_websocket = function (ws) {
    console.log('PREPARING WEBSOCKET')
    ws.onmessage = _on_tour_event;
    ws.onclose = _on_server_side_tour_disconnect;
    //... Might be more initialisation latter ...
}

let disconnect_tour_socket = function() {
    if (tournamentWebSock)
        tournamentWebSock.close()
    tourWebSockID = null;
    tourWebSock = null;
}
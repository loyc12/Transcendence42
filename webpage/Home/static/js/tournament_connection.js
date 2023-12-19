
let tourWebSockID = null;
let tourWebSock = null;

let _on_tour_event = function(event) {
    console.log('User received event from user websocket');
    const data = JSON.parse(event.data);

    if (data.ev === 'connect') {
        console.log('User received message from server after websocket connection : ' + data.msg);
    }
    elif (data.ev === 'game_connect') {
        console.log('Client Received Game connection order from tournament socket')
        reset_default_lobby();
        gameType = data.form.gameType;
        parseInitData(get_default_init_state(gameType));

        gameSockID = data.sockID;
        gameEventID = data.form.eventID;
        gameWebSockPath = _build_tour_ws_path();
        gameWebSock = _connect_to_game_socket(gameWebSockPath);
        _prepare_websocket(gameWebSock);
    }
}

let _build_tour_ws_path = function(sockID) {
    return 'ws://' + window.location.host + '/tournament/ws/' + sockID + '/';
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
    console.error('The server disconnecter USER');
    console.log('Server closed USER websocket connection. Current socket readyState : ');
    user_id = null;
};

let _prepare_tour_websocket = function (ws) {
    console.log('PREPARING WEBSOCKET')
    userWebSock = ws;
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

let tourWebSockID = null;
let tourWebSock = null;
let tourStage1GameData = null;
let tourStage2GameData = null;
let isTournamentStage1 = false;
let tournamentStage1Started = false;
let isTournamentStage2 = false;
let tournamentStage2Started = false;

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
        console.log('_on_tour_event :: data.form.gameMode; : ' + data.form.gameMode);
        console.log('_on_tour_event :: data.stage : ' + data.stage);
        console.log('_on_tour_event :: data.sockID : ' + data.sockID);
        console.log('_on_tour_event :: data.form : ' + data.form);
        console.log('_on_tour_event :: gameType received from data.form.gameType : ' + gameType);
        parseInitData(get_default_init_state(gameType));

        disconnect_socket()

        tourStage1GameData = data;
        isTournamentStage1 = true;
    }
    else if (data.ev === 'brackets') {
        console.log('WoOoW ! received tournament brackets info : ' + data.brackets)
        // loadModule('lobby');
    }
}

// let _build_tour_ws_path = function(sockID) {
function _build_tour_ws_path(sockID) {
    return 'wss://' + window.location.host + '/tournament/ws/' + sockID + '/';
}

let _connect_to_tour_socket = function (tourWebSockPath) {
    let sock;

    console.log('Connecting to TOURNAMENT websocket at : ', tourWebSockPath)
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
    // ws.onopen = _on_open_;
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
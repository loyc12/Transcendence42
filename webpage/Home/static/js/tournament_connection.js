
let wipe_tournament_data = function () {
    console.log('wipe_tournament_data :: CALLED !!')
    tourWebSock = null;
    tourStage1GameData = null;
    tourStage2GameData = null;
    tourStage = null;
    isTournamentStage1 = false;
    tournamentStage1Started = false;
    isTournamentStage2 = false;
    tournamentStage2Started = false
}

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
        console.log('_on_tour_event :: data.stage : ' + data.stage);
        console.log('_on_tour_event :: gameType received from data.form.gameType : ' + gameType);
        parseInitData(get_default_init_state(gameType));

        disconnect_socket()

        let stageNB = data.stage;
        if (stageNB == '1') {
            console.log('_on_tour_event :: stageNB is 1 str : ' + stageNB)
            isTournament = true;
            tourStage2GameData = null;
            tourStage = 'lobbyStage1';
            tourStage1GameData = data;
            isTournamentStage1 = true;
        }
        else if (stageNB == '2') {
            console.log('_on_tour_event :: stageNB is 2 str : ' + stageNB)
            isTournament = true;
            tourStage1GameData = null;
            tourStage = 'lobbyStage2';
            tourStage2GameData = data;
            isTournamentStage2 = true;
        }
        else
            console.log('_on_tour_event :: stageNB is neither 1 or 2 str : ' + stageNB)
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
    console.log('Connecting to TOURNAMENT websocket at : ', tourWebSockPath)
    try {
        sock = new WebSocket(tourWebSockPath);
    } catch (err) {
        alert('Failed To connect to server TOURNAMENT websocket.')
    }
    console.log('SUCCESSFULLY connected to web socket ' + sock);
    return sock;
}


let _on_server_side_tour_disconnect = function(e) {
    console.error('The server disconnecter tournament');
    console.log('Server closed tournament websocket connection. Current socket readyState : ');
    // user_id = null;
    disconnect_socket();
    wipe_tournament_data()
};

let _prepare_tour_websocket = function (ws) {
    console.log('PREPARING WEBSOCKET')
    // ws.onopen = _on_open_;
    ws.onmessage = _on_tour_event;
    ws.onclose = _on_server_side_tour_disconnect;
    //... Might be more initialisation latter ...
}

let disconnect_tour_socket = function() {
    console.log('disconnect_tour_socket CALLED !')
    if (tourWebSock)
        tourWebSock.close()
    tourWebSockID = null;
    tourWebSock = null;
}

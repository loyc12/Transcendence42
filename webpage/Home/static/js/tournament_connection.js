
let wipe_tournament_data = function () {
    tourWebSock = null;
    tourStage1GameData = null;
    tourStage2GameData = null;
    tourStage = null;
    isTournament = null;
    isTournamentStage1 = false;
    tournamentStage1Started = false;
    isTournamentStage2 = false;
    tournamentStage2Started = false;
    isGhostLobby = false;

}

let _on_tour_event = function(event) {
    const data = JSON.parse(event.data);

    if (data.ev === 'connect') {
        console.log('User received message from server after tournament websocket connection : ' + data.msg);
    }
    else if (data.ev === 'game_connect') {
        player_is_ready = false;
        reset_default_lobby();
        gameType = data.form.gameMode;
        parseInitData(get_default_init_state('Tournament'));
        disconnect_socket();

        let stageNB = data.stage;
        if (stageNB == '1') {
            isTournament = true;
            tourStage2GameData = null;
            tourStage = 'lobbyStage1';
            tourStage1GameData = data;
            isTournamentStage1 = true;
        }
        else if (stageNB == '2') {
            isTournament = true;
            tourStage1GameData = null;
            tourStage = 'lobbyStage2';
            tourStage2GameData = data;
            isTournamentStage2 = true;
        }
    }
    else if (data.ev === 'brackets') {
    }
    else if (data.ev === 'quitter') {
        loadTournamentQuitterEnding(data);
    }
}

function _build_tour_ws_path(sockID) {
    return 'wss://' + window.location.host + '/tournament/ws/' + sockID + '/';
}

let _connect_to_tour_socket = function (tourWebSockPath) {
    let sock;
    try {
        sock = new WebSocket(tourWebSockPath);
    } catch (err) {
        alert('Failed To connect to server TOURNAMENT websocket.')
    }
    return sock;
}


let _on_server_side_tour_disconnect = function(e) {
    console.error('The server disconnected tournament');
    disconnect_socket();
    wipe_tournament_data();
};

let _prepare_tour_websocket = function (ws) {
    ws.onmessage = _on_tour_event;
    ws.onclose = _on_server_side_tour_disconnect;
}

let disconnect_tour_socket = function() {
    if (tourWebSock)
        tourWebSock.close();
    tourWebSockID = null;
    tourWebSock = null;
}

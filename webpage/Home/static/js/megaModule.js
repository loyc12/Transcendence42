
var gameSockID = null;
var gameEventID = null;
var gameWebSockPath = null;
var gameWebSock = null;


// KEY EVENTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
let _send_player_keyevent = function(key) {
    payload = JSON.stringify({
        'ev': KEYPRESS,
        'key': key
    })
    gameWebSock.send(payload)
}

// WEBSOCKETS  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
let _get_websocket_path = function(sockID) {
    return 'wss://' + window.location.host + '/game/ws/' + sockID + '/';
}


// THIS FUNCTION CALLED FOR EACH MESSAGE SENT BY THE SERVER
// THROUGH THE WEBSOCKET FOR THIS CLIENT.
let _on_game_event = function(event) {

    const data = JSON.parse(event.data);

    if (data.ev === 'up') {
        // Called by websocket with event type 'up' for every update during a game.
        parseUpdateData(data.state)
    }
    else if (data.ev === "init") {
        // Sent ONCE at the begining of lobby phase with data required to render a game.
        console.log('data.init.orientation[0] + ' + data.init.orientations[0]);
        parseInitData(data.init)
        console.log('- - - Received INIT : ' + data.init);
    }
    else if (data.ev === 'connection') {
        /// Triggered in lobby phase when either the current user gets connected to a game socket
        /// or another user has connected to the same game.
        let players = data.player_list;
        let i = 0
        for (p of players) {
            ++i;
            console.log('Player ' + i + ' : ' + p);
            console.log(`Player ${i} :: login : ` + p.login)
            console.log(`Player ${i} :: img : ` + p.img)
            console.log(`Player ${i} :: ready : ` + p.ready)
        }
        update_player_info(data.player_list)
    }


    else if (data.ev === "start") {
        // Trigger event received when game should start. Sent by websocket when all players have signaled their readiness.
        console.log('RECEIVED START SIGNAL FROM SERVER !');
        player_is_ready = false;
        loadGame()
    }
    else if (data.ev === "end") {
        // Trigger event received when game should start. Sent by websocket when all players have signaled their readiness.
        console.log('RECEIVED END SIGNAL FROM SERVER !');
        console.log('data.end_state : ' + data.end_state);
        loadEndGame(data.end_state);
    }
}

let _on_server_side_disconnect = function(e) {
    console.error('The server disconnecter you');
    gameWebSock = null;
    gameSockID = null;
    gameEventID = null;
    gameWebSockPath = null;
    if (isTournamentStage1 && !tournamentStage1Started) {
        gameSockID = tourStage1GameData.sockID;
        gameEventID = tourStage1GameData.form.eventID;
        gameWebSockPath = _get_websocket_path(gameSockID);
        gameWebSock = _connect_to_game_socket(gameWebSockPath);
        _prepare_websocket(gameWebSock);
        tournamentStage1Started = true;
    }
    else if (isTournamentStage2 && !tournamentStage2Started) {
        gameSockID = tourStage2GameData.sockID;
        gameEventID = tourStage2GameData.form.eventID;
        gameWebSockPath = _get_websocket_path(gameSockID);
        gameWebSock = _connect_to_game_socket(gameWebSockPath);
        _prepare_websocket(gameWebSock);
        tournamentStage2Started = true;
    }
    else {
        console.log('_on_server_side_disconnect :: Game Socket disconnected regular game ?!');
        console.log('_on_server_side_disconnect :: Game Socket disconnected :: isTournamentStage1 : ' + isTournamentStage1)
        console.log('_on_server_side_disconnect :: Game Socket disconnected :: isTournamentStage2 : ' + isTournamentStage2)
        console.log('_on_server_side_disconnect :: Game Socket disconnected :: tournamentStage1Started : ' + tournamentStage1Started)
        console.log('_on_server_side_disconnect :: Game Socket disconnected :: tournamentStage2Started : ' + tournamentStage2Started)
    }
};

let _connect_to_game_socket = function (gameWebSockPath) {
    let sock;

    console.log('Connecting to websocket at : ', gameWebSockPath)
    try {
        sock = new WebSocket(gameWebSockPath);
    } catch (err) {
        alert('Failed To connect to server websocket.')
    }
    return sock;
}


let _prepare_websocket = function (ws) {
    gameWebSock = ws;
    ws.onmessage = _on_game_event;
    ws.onclose = _on_server_side_disconnect;
}

let disconnect_socket = function() {

    if (gameWebSock != null) {
        gameWebSock.close()
        gameSockID = null;
        gameWebSockPath = null;
    }
    deactivatePlayerControler()
}

let get_default_init_state = function(gameType) {
    if (! gameType in allInitGameStates)
        alert(`gameType ${gameType} not found in allInitGameStates`);
    return allInitGameStates.get(gameType);
}

let is_requesting_join_game = false;
let loadMegaModule = function (gameType) {

    // check_user_is_connected();

    if (is_requesting_join_game)
        return;
    // Send HTTP POST request to get matched to a game in the MatchMaker or create a new one
    if (gameWebSock != null) {
        alert("You can't connect to a game while already connected to another.")
        throw new EvalError("You can't connect to a game while already connected to another.");
    }
    is_requesting_join_game = true;

    player_is_ready = false;

    // Resets lobby state
    reset_default_lobby();

    /// Find the default init game state from defs.js based on gameType given,
    // set it as global currentGameInfo and render it in canvas (even if canvas is hidden).
    console.log(get_default_init_state(gameType));
    parseInitData(get_default_init_state(gameType));

    //DEBUG
    printCurrentParam(currentGameInfo);

    // Will draw the gameType's default init state
    updateCanvas(currentGameInfo);

    // Request the server to join a game of gameType. Player will be placed in MatchMaker first.
    // TOURNAMENT
    request_join_game(gameType)
        .then(function (gameData) {
            /// Officially connect to the game socket in the game group given by the server at sockID.
            if (!gameData.sockID)
                throw new EvalError('Request Join Game FAILED !');
            gameSockID = gameData.sockID;
            gameWebSockPath = _get_websocket_path(gameData.sockID);

            // Setting global var isTournament
            if (gameData.gameMode === 'Tournament')
            {
                tourWebSockID = gameData.tourSockID;
                tourWebSockPath = _build_tour_ws_path(tourWebSockID);
                tourWebSock = _connect_to_tour_socket(tourWebSockPath);
                _prepare_tour_websocket(tourWebSock);
                isTournament = true;
            }
            else if (!isTournament){
                wipe_tournament_data();
                isTournament = false;
            }

            // Load the lobby page.
            location.hash = 'init';
            loadModule('lobby');

            return _connect_to_game_socket(gameWebSockPath);
        })
        .then(function (gameWebSock) {
            /// Set websocket callbacks
            _prepare_websocket(gameWebSock);
        })
        .catch(e => {
            console.error('Exeption while requesting to join game : ' + e)
        })
    is_requesting_join_game = false;
}

let loadGame = function() {
    loadModule('game');
    activatePlayerControler();

}

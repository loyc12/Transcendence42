
var gameSockID = null;
var gameWebSockPath = null;
var gameWebSock = null;



let _send_player_keyevent = function(key) {
    payload = JSON.stringify({
        'ev': KEYPRESS,
        'key': key
    })
    gameWebSock.send(payload)
}


let _get_websocket_path = function(sockID) {
    return 'ws://' + window.location.host + '/game/ws/' + sockID + '/';
}


// THIS FUNCTION CALLED FOR EACH MESSAGE SEND BY THE SERVER
// THROUGH THE WEBSOCKET FOR THIS CLIENT.
let _on_game_event = function(event) {

    console.log('Client RECEIVED evenv : ' + event)

    const data = JSON.parse(event.data);

    if (data.ev === 'up') {
        // Called by websocket with event type 'up' for every update during a game.
        parseUpdateData(data.state)
    }
    else if (data.ev === "init") {
        // Sent ONCE at the begining of lobby phase with data required to render a game.
        // See PingPongRebound/json-template.json, section : getInitInfo()
        parseInitData(data.init)
    }
    else if (data.ev === 'connection') {
        /// Triggered in lobby phase when either the current user gets connected to a game socket
        /// or another user has connected to the same game. 
        // TODO: Should trigger a function to update the players list and infos in lobby phase
        let players = data.player_list;
        let i = 0
        for (p of players) {
            ++i;
            console.log('Player ' + i + ' : ' + p)
        }
        //...
    }
    else if (data.ev === "player_info") {
        // Sent ONCE after lobby phase at the begining of a game, when all players have declared themselves ready,
        // with data describing active players.
        parsePlayersInfo(data.info);
    }
    else if (data.ev === "start") {
        // Trigger event received when game should start. Sent by websocket when all players have signaled their readiness.
        console.log('RECEIVED START SIGNAL FROM SERVER !');
        loadGame()
    }
}

let _on_server_side_disconnect = function(e) {
    console.error('The server disconnecter you');
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
    //... Might be more initialisation latter ...
}

function disconnect_socket() {

    console.log('Entered disconnect_socket')
    if (gameWebSock != null) {
        console.log('Trying to close websocket connection')
        gameWebSock.close()
        console.log('Maybe closed websocket ? is closed ?' + gameWebSock.CLOSED);
        
        gameSockID = null;
        gameWebSockPath = null;
        gameWebSock = null;
        /// TODO: Potentially wait for socket to close and do something ...
    }
    deactivatePlayerControler()
}

let get_default_init_state = function(gameType) {
    console.log(allInitGameStates);
    if (! gameType in allInitGameStates)
        alert(`gameType ${gameType} not found in allInitGameStates`);
    else
        console.log(`gameType ${gameType} found in allInitGameStates : ` + allInitGameStates.get(gameType));
    return allInitGameStates.get(gameType);
}

let loadMegaModule = function (gameType) {
    
    console.log('LOAD MEGA MODULE STARTING GAME JOIN PROCESS !')
    // Send HTTP POST request to get matched to a game in the MatchMaker or create a new one
    if (gameWebSock != null) {
        alert("You can't connect to a game while already connected to another.")
        throw new EvalError("You can't connect to a game while already connected to another.");
    }

    // Load the lobby page.
    loadModule('lobby');
    
    /// Find the default init game state from defs.js based on gameType given,
    // set it as global currentGameInfo and render it in canvas (even if canvas is hidden).
    console.log(`init state for gameType ${gameType} : `);
    console.log(get_default_init_state(gameType));
    parseInitData(get_default_init_state(gameType));
    printCurrentParam(currentGameInfo);

    // Will draw the gameType's default init state 
    updateCanvas(currentGameInfo);

    // Request the server to join a game of gameType. Player will be placed in MatchMaker first.
    request_join_game(gameType)
    .then(function (sockID) {
        /// Officially connect to the game socket in the game group given by the server at sockID.
        if (!sockID)
            throw new EvalError('Request Join Game FAILED !');
        gameSockID = sockID;
        gameWebSockPath = _get_websocket_path(sockID);
        return _connect_to_game_socket(gameWebSockPath);
    })
    .then(function (gameWebSock) {
        /// Set websocket callbacks
        _prepare_websocket(gameWebSock);
        console.log('Connection to websocket SUCCESSFUL !')
    })
    .catch(e => {
        //alert('You failed to join a game for the following reason : ' + e)
        console.log('Exeption while requesting to join game : ' + e)
    })
    
    /// Enable player keypress handler
    // TODO: SHOULD WAIT UNTIL GAME START SIGNAL IS SENT BY WEBSOCKET.
    // activatePlayerControler()
}

let loadGame = function() {
    console.log('Load loadGame')
    loadModule('game');
    activatePlayerControler();
    
    // document.getElementById('lobby').style.display = 'block';
    
}
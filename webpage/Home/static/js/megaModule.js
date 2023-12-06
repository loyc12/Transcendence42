
var gameSockID = null;
var gameWebSockPath = null;
var gameWebSock = null;

let _get_websocket_path = function(sockID) {
    return 'ws://' + window.location.host + '/game/ws/' + sockID + '/';
}

let _on_game_event = function(event) {
    const data = JSON.parse(event.data);
    console.log('ev : ' + data.ev)
    console.log('ev === "connection" ? ' + (data.ev === 'connection'))
    if (data.ev === 'up') {
        console.log('UPDATE event received from websocket.');
        console.log(data)
        //...
    }
    else if (data.ev === 'connection') {
        /// Triggered when either the current user gets connected to a game socket
        /// or another user has connected to the same game.
        /// data.players
        console.log('PLAYERS event received from websocket.');
        console.log(data)
        let players = data.player_list;
        let i = 0
        for (p of players) {
            ++i;
            console.log('Player ' + i + ' : ' + p)
        }
        //...
    }
    else if (data.ev === "initGameInfo") {
        console.log('INIT GAME INFO event received from websocket.');
        console.log(data)
    }
    //...
}

let _on_server_side_disconnect = function(e) {
    console.error('The server disconnecter you');
};

let _connect_to_game_socket = function (gameWebSockPath) {
    let sock;

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

let disconnect_socket = function () {

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
}

let loadMegaModule = function (gameType) {
    
    console.log('LOAD MEGA MODULE STARTING GAME JOIN PROCESS !')
    // Send HTTP POST request to get matched to a game in the MatchMaker or create a new one
    if (gameWebSock != null) {
        alert("You can't connect to a game while already connected to another.")
        throw new EvalError("You can't connect to a game while already connected to another.");
    }

    request_join_game(gameType)
    .then(function (sockID) {
        //gameWebSockPath = _get_websocket_path(sockID);
        if (!sockID)
            throw new EvalError('Request Join Game FAILED !');
        gameSockID = sockID;
        gameWebSockPath = _get_websocket_path(sockID);
        return _connect_to_game_socket(gameWebSockPath);
    })
    .then(function (gameWebSock) {
        _prepare_websocket(gameWebSock);
    })
    .catch(e => {
        //alert('You failed to join a game for the following reason : ' + e)
        console.log('Exeption while requesting to join game : ' + e)
    })
    //return;
    //console.log('gameWebSockPath : ' + gameWebSockPath)
    //gameWebSock = _connect_to_game_socket(gameWebSockPath)
    //console.log('Connection to websocket SUCCESSFUL !')
    //_prepare_websocket(gameWebSock);
    
    // TODO: Enable Start/Ready button click
    // ...
}

var gameSockID = null;
var gameWebSockPath = null;
var gameWebSock = null;


// keyboard keys
// let UP =     'up';
// let DOWN =   'dn';
// let LEFT =   'lf';
// let RIGHT =  'rt';
// let SPACE =  ' ';

// // keypad keys
// let KW = 'w';
// let KS = 's';
// let KA = 'a';
// let KD = 'd';
// let NZERO = '0';

// let START = 'start_game';
// let CLOSE = 'end_game';
// let KEYPRESS = 'key_press';
// let ESCAPE = null;
// let RETURN = null;


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


// THIS FUNCTION IS THE LANDING CALLBACK METHOD FOR 
// WEBSOCKET MESSAGES TO THE CLIENT.
let _on_game_event = function(event) {
    const data = JSON.parse(event.data);
    // console.log('ev : ' + data.ev)
    // console.log('ev === "connection" ? ' + (data.ev === 'connection'))
    if (data.ev === 'up') {
        // console.log('UPDATE event received from websocket.');
        // console.log(data)
        parseUpdateData(data.state)
        // TODO: Render updated game state
    }
    else if (data.ev === 'connection') {
        /// Triggered when either the current user gets connected to a game socket
        /// or another user has connected to the same game.
        /// data.players
        // console.log('PLAYERS event received from websocket.');
        // console.log(data)
        let players = data.player_list;
        let i = 0
        for (p of players) {
            ++i;
            console.log('Player ' + i + ' : ' + p)
        }
        //...
    }
    else if (data.ev === "init") {
        // console.log('INIT GAME INFO event received from websocket.');
        // console.log(data)
        parseInitData(data.init)
    }
    else if (data.ev === "pinfo") {
        parsePlayersInfo(data.info);
    }
    //...
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
}

let loadMegaModule = function (gameType) {
    
    console.log('LOAD MEGA MODULE STARTING GAME JOIN PROCESS !')
    // Send HTTP POST request to get matched to a game in the MatchMaker or create a new one
    if (gameWebSock != null) {
        alert("You can't connect to a game while already connected to another.")
        throw new EvalError("You can't connect to a game while already connected to another.");
    }
    
    console.log('From MegaModule gameType : ' + gameType)
    parseInitData(initPongParam);
    printCurrentParam(currentGameInfo);
    loadModule('lobby');
    // renderCanvas(currentGameInfo);
    updateCanvas(currentGameInfo);
    // return ;

    request_join_game(gameType)
    .then(function (sockID) {
        if (!sockID)
            throw new EvalError('Request Join Game FAILED !');
        gameSockID = sockID;
        gameWebSockPath = _get_websocket_path(sockID);
        return _connect_to_game_socket(gameWebSockPath);
    })
    .then(function (gameWebSock) {
        if (gameWebSock.CONNECTING)
            console.log('websocket is connecting')
        if (gameWebSock.OPEN)
            console.log('websocket is open for comm')
        if (gameWebSock.CLOSING)
            console.log('websocket is closing')
        _prepare_websocket(gameWebSock);
        console.log('Connection to websocket SUCCESSFUL !')
    })
    .catch(e => {
        //alert('You failed to join a game for the following reason : ' + e)
        console.log('Exeption while requesting to join game : ' + e)
    })
    //return;
    
    // TODO: Enable Start/Ready button click
    // ...
    
    /// Enable player keypress handler
    activatePlayerControler()
}
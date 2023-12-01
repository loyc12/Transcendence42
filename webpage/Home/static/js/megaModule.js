
let sockID;
let webSockPath;
let webSock;

let _get_websocket_path = function(sockID) {
    return 'ws://' + window.location.host + '/game/ws/' + sockID + '/';
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
    else if (data.ev === "initGameInfo") {
        console.log('INIT GAME INFO event received from websocket.');
        console.log(data)
    }
    //...
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
    webSock.onclose = _on_server_side_disconnect;
    //... Might be more initialisation latter ...
}

let loadMegaModule = function (gameType) {
    
    console.log('LOAD MEGA MODULE STARTING GAME JOIN PROCESS !')
    // Send HTTP POST request to get matched to a game in the MatchMaker or create a new one
    request_join_game(gameType)
    .then(function (sockID) {
        //webSockPath = _get_websocket_path(sockID);
        if (!sockID)
            alert('Request Join Game FAILED !')
        webSockPath = _get_websocket_path(sockID);
        return _connect_to_game_socket(webSockPath);
    })
    .then(function (webSock) {
        _prepare_websocket(webSock);
    })
    .catch(e => {
        console.log('Exeption while requesting to join game : ' + e)
    })
    //return;
    //console.log('webSockPath : ' + webSockPath)
    //webSock = _connect_to_game_socket(webSockPath)
    //console.log('Connection to websocket SUCCESSFUL !')
    //_prepare_websocket(webSock);
    
    // TODO: Enable Start/Ready button click
    // ...
}
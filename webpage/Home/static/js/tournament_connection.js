
let tournamentWebSockID = null;
let tournamentWebSock = null;

let _on_tournament_event = function(event) {
    console.log('tournament received event from tournament websocket');
    const data = JSON.parse(event.data);

    if (data.ev === 'connect')
        console.log('tournament received message from server after websocket connection : ' + data.msg);
}

let _on_tournament_close_disconnect = function (event) {
    console.error('Server disconnected tournament websocket');
}

let _build_tournament_ws_path = function(sockID) {
    return 'ws://' + window.location.host + '/tournament/ws/' + sockID + '/';
}

let _connect_to_tournament_socket = function (tournamentWebSockPath) {
    let sock;

    console.log('Connecting to tournament websocket at : ', tournamentWebSockPath)
    try {
        sock = new WebSocket(tournamentWebSockPath);
    } catch (err) {
        alert('Failed To connect to server tournament websocket.')
    }
    return sock;
}

let _on_server_side_tournament_disconnect = function(e) {
    console.error('The server disconnecter tournament');
    console.log('Server closed tournament websocket connection. Current socket readyState : ');
    tournament_id = null;
};

let _prepare_tournament_websocket = function (ws) {
    console.log('PREPARING WEBSOCKET')
    tournamentWebSock = ws;
    ws.onmessage = _on_tournament_event;
    ws.onclose = _on_tournament_close_disconnect;
    //... Might be more initialisation latter ...
}


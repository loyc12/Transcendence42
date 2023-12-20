
let userWebSockID = null;
let userWebSock = null;

let _on_user_event = function(event) {
    console.log('User received event from user websocket');
    const data = JSON.parse(event.data);

    if (data.ev === 'connect')
        console.log('User received message from server after websocket connection : ' + data.msg);
}

let _on_close_disconnect = function (event) {
    console.error('Server disconnected user websocket');
}



let _build_user_ws_path = function(sockID) {
    return 'wss://' + window.location.host + '/users/ws/' + sockID + '/';
}

let _connect_to_user_socket = function (userWebSockPath) {
    let sock;

    console.log('Connecting to USER websocket at : ', userWebSockPath)
    try {
        sock = new WebSocket(userWebSockPath);
    } catch (err) {
        alert('Failed To connect to server USER websocket.')
    }
    return sock;
}


let _on_server_side_user_disconnect = function(e) {
    console.error('The server disconnecter USER');
    console.log('Server closed USER websocket connection. Current socket readyState : ');
    user_id = null;
    
};

let _prepare_user_websocket = function (ws) {
    console.log('PREPARING WEBSOCKET')
    userWebSock = ws;
    ws.onmessage = _on_user_event;
    ws.onclose = _on_close_disconnect;
    //... Might be more initialisation latter ...
}


if (user_id != null) {
    // build websocket path
    userWebSockID = ('USOCK' + user_id);
    let sockPath = _build_user_ws_path(userWebSockID);
    
    // connect to websocket
    userWebSock = _connect_to_user_socket(sockPath);

    // setup websocket
    _prepare_user_websocket(userWebSock);
    console.log('USER WEBSOCKET SUCCESSFULLY CONNECTED');
}
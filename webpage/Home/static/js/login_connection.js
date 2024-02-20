
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
    fetch_user_logout()
    userDisconnectedSocket = true;
}

let _build_user_ws_path = function(sockID) {
    return 'wss://' + window.location.host + '/users/ws/' + sockID + '/';
}

let _connect_to_user_socket = function (userWebSockPath) {
    let sock;

    try {
        sock = new WebSocket(userWebSockPath);
    } catch (err) {
        alert('Failed To connect to server USER websocket.')
    }
    return sock;
}


let fetch_user_logout = function () {

    fetch('https://' + window.location.host + '/users/profile/logout')
    .then (data => {

      data.text().then(text => {
            console.log('Force logout status returned : ' + text)
        })
    })
}

let disconnect_user_socket = function() {

    fetch_user_logout()
    if (userWebSock != null) {
        userWebSock.close()

        userWebSock = null;
        userWebSockID = null;
    }
    userDisconnectedSocket = true;
}

let _on_server_side_user_disconnect = function(e) {
    console.error('The server disconnecter USER');
    user_id = null;

};

let _prepare_user_websocket = function (ws) {
    userWebSock = ws;
    ws.onmessage = _on_user_event;
    ws.onclose = _on_close_disconnect;
}

let login_click_disabled = false;
let initiate_42_login = function (login_addr) {

    if (login_click_disabled) {
        console.log('LOGIN CLICK BLOCKED !! Your welcome.');
        return;
    }
    console.log('Trying to redirect to : ' + login_addr + ' while login_click_disabled is ' + login_click_disabled);
    login_click_disabled = true;
    window.location.replace(login_addr);
}


if (user_id != null) {
    // build websocket path

    userWebSockID = ('USOCK' + user_id);
    let sockPath = _build_user_ws_path(userWebSockID);

    // connect to websocket
    userWebSock = _connect_to_user_socket(sockPath);

    // setup websocket
    _prepare_user_websocket(userWebSock);
}
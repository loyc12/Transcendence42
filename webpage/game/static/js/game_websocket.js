console.log("WOW")

const PLAYER1 = 1;
const PLAYER2 = 2;
const PLAYER3 = 3;
const PLAYER4 = 4;

const VALID_KEYEVENTS = ['w', 'a', 's', 'd', 'ArrowUp', 'ArrowLeft', 'ArrowDown', 'ArrowRight'];

let sock;
let sock_connected = false;
let player_id = 0;


/// Possible client event_type values :
//  - start_game
//  - keypress
//  - keyrelease
//  - ...
//  - end_game

class ClientEvent {
    key_name;
    key_code;
}

let connect_to_game_socket = function () {
    const elem = document.getElementById('game-id');
    console.log(elem)
    const game_id = JSON.parse(elem.textContent);
    const ws_path = 'ws://' + window.location.host + '/game/ws/' + game_id + '/';
    console.log('ws_path : ' + ws_path);
    try {
        sock = new WebSocket(ws_path);
        sock_connected = true;
        console.log(sock)
        sock.onmessage = on_message;
        sock.onclose = on_close;
    } catch (err) {
        alert('Failed To connect to server websocket.')
    }
}

let on_message = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    console.log('event_type : ' + data.event_type)
    if (data.event_type === "init_message") {
        console.log('AUTHENTIC init_msg from websocket.');
        document.querySelector('#ws_init_msg').innerHTML = data.msg;
    }
    else {
       document.querySelector('#ws_init_msg').innerHTML = data.msg;
    }
}

let on_close = function(e) {
    console.error('Chat socket closed unexpectedly');
};



///// Key event callbacks //////////////////////////////////

let is_valid_key = function (key) {
    return (VALID_KEYEVENTS.includes(key));
}

let send_message = function (payload) {
    if (sock_connected) {
        try {
            sock.send(payload)
        } catch (e) {
            alert('Failed to send message to server.')
            return false;
        }
    }
    else {
        alert('Trying to send message to server while not connected.')
        return false;
    }
    return true;
}

let create_keyevent_payload = function (keyevent, key) {
    return (JSON.stringify({
            'event_type': keyevent,
            'details': {
                'key': key
            }
        })
    )
}

document.onkeydown = function (event) {
    if (event.repeat || ! is_valid_key(event.key))
        return;
    console.log('KeyDown event.code : ' + event.code + ' event.key : ' + event.key + ' event.repeat : ' + event.repeat);

    event_payload = create_keyevent_payload('keypress', event.key);
    console.log('event payload : ' + event_payload)
    if (! send_message(event_payload))
        console.log('Failed to send key event');
    else
        console.log('Sent key event successfully');
}

document.onkeyup = function (event) {
    if (event.repeat || ! is_valid_key(event.key))
        return;
    console.log('KeyUp event.code : ' + event.code + ' event.key : ' + event.key + ' event.repeat : ' + event.repeat)
    
    //event_payload = JSON.stringify({
    //    'event_type': 'keypress',
    //    'detail': {
    //        'key': event.key
    //    }
    //});
    event_payload = create_keyevent_payload('keyrelease', event.key);
    console.log('event payload : ' + event_payload)
    if (! send_message(event_payload))
        console.log('Failed to send key event');
    else
        console.log('Sent key event successfully');
}


//connect_to_game_socket()
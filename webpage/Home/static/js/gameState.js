// const canvas = document.getElementById('canvas');
// const ctx = canvas.getContext('2d');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

//get init_data from gameState.js

// Store the initial dimensions0
const initialWidth = canvas.width;
const initialHeight = canvas.height;

currentWidth = canvas.width;
currentHeight = canvas.height;

// This value holds the initState of the current game being played.
// Defaults to gameType Pong.
// let currentGameInfo = initPongParam;


// Afficher les valeurs dans la console
function printCurrentParam (currentGameInfo) {
    console.log('Game Type:', currentGameInfo.gameType);
    console.log('Width:', currentGameInfo.sizeInfo.width);
    console.log('Height:', currentGameInfo.sizeInfo.height);
    console.log('Racket Size:', currentGameInfo.sizeInfo.sRacket);
    console.log('Racket:', currentGameInfo.racketCount);
    for (let i = 0; i < currentGameInfo.racketCount; i++) {
        let racketX = currentGameInfo.update.racketPos[2*i];
        let racketY = currentGameInfo.update.racketPos[2*i + 1];
        let ori = currentGameInfo.orientations[i];
        
        // Vérifiez si la position de raquette est 'x'
        if (racketX !== 'x' && racketX !== 'y') {
            console.log(`Position de raquette ${i + 1}: x=${racketX}, y=${racketY}`);
        } 
        if (ori === 'x') {
            console.log(`raquette ${i + 1} orientation Horizontal`);
        }
        else if (ori === 'y') {
            console.log(`raquette ${i + 1} orientation Vertical`);
        }
    }
    console.log('Ball:', currentGameInfo.ballPos);
    console.log('Ball Size:', currentGameInfo.sizeInfo.sBall);
    console.log('Team:', currentGameInfo.teamCount);
}


let setCanvasSize = function () {
    const parent = canvas.parentElement

    //Use initial dimensions if the parent is smaller
    canvas.width = Math.min(initialWidth, parent.clientWidth);
    canvas.height = Math.min(initialHeight, parent.clientHeight);
    
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}


const prevent_keyset = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'];
// Function called on player keypress events.
// It sends the event through the websocket to be handled by by GameManager server side.
let _player_event_handler = function (event) {

    // Repeated keys are refused
    if (event.repeat) {
        return;
    }
    console.log('event keypress : ' + event.key )
    if (prevent_keyset.indexOf(event.code) > -1) {
        console.log('PREVENTING DEFAULT');
        event.preventDefault();
    }

    // Move paddle up (keyCode 38 or W key)
    if ( event.key === 'w') {
        console.log('W');
        _send_player_keyevent(KW);
    }
    
    // Move paddle down (keyCode 40 or S key)
    else if ( event.key === 's') {
        console.log('S');
        _send_player_keyevent(KS);
    }
    
    // Move paddle left (keyCode 37 or A key)
    else if ( event.key === 'a') {
        console.log('A');
        _send_player_keyevent(KA);
    }
    
    // Move paddle right (keyCode 39 or D key)
    else if ( event.key === 'd') {
        console.log('D');
        _send_player_keyevent(KD);
    }
    
    else if (event.key === ' ') {
        console.log('<SPACE> : event.code : ' + event.code + ', event.key : ' + event.key)
        _send_player_keyevent(SPACE);
    }

    // Move paddle up (keyCode 38 or W key)
    else if (event.key === "ArrowUp") {
        console.log('ArrowUp');
        _send_player_keyevent(UP);
    }
    
    // Move paddle down (keyCode 40 or S key)
    else if (event.key === "ArrowDown") {
        console.log('ArrowDown');
        _send_player_keyevent(DOWN);
    }

    // Move paddle left (keyCode 37 or A key)
    else if (event.key === "ArrowLeft") {
        console.log('ArrowLeft');
        _send_player_keyevent(LEFT)
    }
    
    // Move paddle right (keyCode 39 or D key)
    else if (event.key === "ArrowRight") {
        console.log('ArrowRight');
        _send_player_keyevent(RIGHT);
    }

    else if (event.key === '0') {
        console.log('Numpad 0')
        _send_player_keyevent(NZERO);
    }

    
}

let activatePlayerControler = function () {
    document.addEventListener("keydown", _player_event_handler);
}

let deactivatePlayerControler = function () {
    document.removeEventListener("keydown", _player_event_handler);
}

/// SETUP currentGameInfo GLOBAL VARIABLE defined in defs.js
function parseInitData (init_data) {
    //curentData = init_data;
    if (! 'update' in init_data)
        alert("ERROR: initData received is missing the 'update' struct.")
    const { width, height } = init_data.sizeInfo;
    currentGameInfo = init_data;
    
    canvas.width = width;
    canvas.height = height;
    
    /// Pre calculations used in rendering functions
    currentGameInfo.racketSize = init_data.sizeInfo.sRacket;
    currentGameInfo.ballSize = init_data.sizeInfo.sBall;

    currentGameInfo.offsets = [];
    currentGameInfo.widths = [];
    currentGameInfo.heights = [];
    for (ori of init_data.orientations) {
        if (ori === 'x') {
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sRacket * 0.5));
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sBall * 0.5));
            currentGameInfo.widths.push()
        } else if (ori === 'y') {
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sBall * 0.5));
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sRacket * 0.5));
        }
    }
}


// Function to parse update data. 
let parseUpdateData = function (update) {
    currentGameInfo.update = update;
    updateCanvas(currentGameInfo);
}

// function called by 
let parsePlayersInfo = function(info) {
    console.log('Players info : ', info);
    /// TODO: Deal with players info ...
}
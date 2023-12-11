// const canvas = document.getElementById('canvas');
// const ctx = canvas.getContext('2d');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

//get init_data from gameState.js

// Store the initial dimensions
const initialWidth = canvas.width;
const initialHeight = canvas.height;

let currentWidth = canvas.width;
let currentHeight = canvas.height;

// This value holds the initState of the current game being played.
// Defaults to gameType Pong.
let currentGameInfo = initPongParam;


// Afficher les valeurs dans la console
let printCurrentParam = function () {
    console.log('Game Type:', initParam.gameType);
    console.log('Width:', initParam.sizeInfo.width);
    console.log('Height:', initParam.sizeInfo.height);
    console.log('Racket Size:', initParam.sizeInfo.sRacket);
    console.log('Racket:', initParam.racketCount);
    for (let i = 0; i < initParam.racketInitPos.length; i += 3) {
        let racketX = initParam.racketInitPos[i];
        let racketY = initParam.racketInitPos[i + 1];
        
        // Vérifiez si la position de raquette est 'x'
        if (racketX !== 'x' && racketX !== 'y') {
            console.log(`Position de raquette ${i / 3 + 1}: x=${racketX}, y=${racketY}`);
        } 
        if (initParam.racketInitPos[i + 2] === 'x') {
            console.log(`raquette ${i / 3 + 1} orientation Horizontal`);
        }
        if (initParam.racketInitPos[i + 2] === 'y') {
            console.log(`raquette ${i / 3 + 1} orientation Vertical`);
        }
    }
    console.log('Ball:', initParam.ballInitPos);
    console.log('Ball Size:', initParam.sizeInfo.sBall);
    console.log('Team:', initParam.teamCount);
}

// DEBUG
printCurrentParam()

let setCanvasSize = function () {
    const parent = canvas.parentElement

    //Use initial dimensions if the parent is smaller
    canvas.width = Math.min(initialWidth, parent.clientWidth);
    canvas.height = Math.min(initialHeight, parent.clientHeight);
    
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}
// setCanvasSize();

let _player_event_handler = function (event) {
    //paddle1
    // Move paddle up (keyCode 38 or W key)
    if (event.key === "ArrowUp") {// && paddle1.y > 0) {
        console.log('ArrowUp');
        _send_player_keyevent(UP);
        //paddle1.y -= paddle1.speed;
    }
    
    // Move paddle down (keyCode 40 or S key)
    if (event.key === "ArrowDown") {// && paddle1.y < canvas.height - paddle1.height) {
        console.log('ArrowDown');
        _send_player_keyevent(DOWN);
        // console.log('ArrowDown');
        // paddle1.y += paddle1.speed;
    }

    // Move paddle left (keyCode 37 or A key)
    if (event.key === "ArrowLeft") {// && paddle1.x > 0) {
        console.log('ArrowLeft');
        _send_player_keyevent(LEFT)
        //paddle1.x -= paddle1.speed;
    }
    
    // Move paddle right (keyCode 39 or D key)
    if (event.key === "ArrowRight") {// && paddle1.x < canvas.width - paddle1.width) {
        console.log('ArrowRight');
        _send_player_keyevent(RIGHT);
        // paddle1.x += paddle1.speed;
    }
    
    // paddle2
    // Move paddle up (keyCode 38 or W key)
    if ( event.key === 'w') {// && paddle2.y > 0) {
        console.log('W');
        _send_player_keyevent(KW);
        // paddle2.y -= paddle2.speed;
    }
    
    // Move paddle down (keyCode 40 or S key)
    if ( event.key === 's') {// && paddle2.y < canvas.height - paddle2.height) {
        console.log('S');
        _send_player_keyevent(KS);
        // paddle2.y += paddle2.speed;
    }
    
    // Move paddle left (keyCode 37 or A key)
    if ( event.key === 'a') {// && paddle2.x > 0) {
        console.log('A');
        _send_player_keyevent(KA);
        // paddle2.x -= paddle2.speed;
    }
    
    // Move paddle right (keyCode 39 or D key)
    if ( event.key === 'd') {// && paddle2.x < canvas.width - paddle2.width) {
        console.log('D');
        _send_player_keyevent(KD);
        // paddle2.x += paddle2.speed;
    }
}

let activatePlayerControler = function () {
    document.addEventListener("keydown", _player_event_handler);
}

let deactivatePlayerControler = function () {
    document.removeEventListener("keydown", _player_event_handler);
}

// let curentData;

/// SETUP currentGameInfo GLOBAL VARIABLE
let parseInitData = function (init_data) {
    //curentData = init_data;
    if (! 'update' in init_data)
        alert("ERROR: initData received is missing the 'update' struct.")
    currentGameInfo = init_data;
    
    /// Pre calculations used in rendering functions
    currentGameInfo.offsets = [];
    for (ori of init_data.orientations) {
        if (ori === 'x') {
            currentGameInfo.offsets.push(-(init_data.sizeInfo.bSize * 0.5));
            currentGameInfo.offsets.push(-(init_data.sizeInfo.rSize * 0.5));
        } else if (ori == 'y') {
            currentGameInfo.offsets.push(-(init_data.sizeInfo.rSize * 0.5));
            currentGameInfo.offsets.push(-(init_data.sizeInfo.bSize * 0.5));
        }
    }
    currentGameInfo.ballOffset = -(currentGameInfo.sizeInfo.bSize * 0.5);    
    currentGameInfo.xRatio = currentWidth * init_data.sizeInfo.wRatio;
    currentGameInfo.yRatio = currentHeight * init_data.sizeInfo.hRatio;
    currentGameInfo.racketSize = init_data.sizeInfo.rSize * init_data.sizeInfo.wRatio;
    currentGameInfo.ballSize = init_data.sizeInfo.bSize * init_data.sizeInfo.hRatio;


//     const initParam = {
//         'gameType': 'Pong', 
//         'sizeInfo': {'width': 2048, 'height': 1024, 
//            'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 
//            'sRacket': 160, 'sBall': 20}, 
//        'racketCount': 2, 
//        'racketInitPos': [20, 512, 'y', 2028, 512, 'y'], 
//        'ballInitPos': [512, 512], 
//        'teamCount': 2
//    };

}


// start update system from any data first 
// Sample update data
// const newData = {'gameID': 1, 'racgketPos': [20, 512, 2028, 512], 'ballPos': [522, 522], 'lastPonger': 0, 'scores': [0, 0]};

// Function to parse update data
let parseUpdateData = function (update) {
    updateCanvas = update
    console.log('parseUpdateData : ' + update)
    const gameId = update.gameID;
    const racketPositions = update.racketPos;
    const ballPosition = update.ballPos;
    const lastPonger = update.lastPonger;
    const scores = update.scores;

    // You can add more processing or rendering logic based on this parsed data
    console.log('Update Game ID:', gameId);
    console.log('Update Racket Positions:', racketPositions);
    console.log('Update Ball Position:', ballPosition);
    console.log('Update Last Ponger:', lastPonger);
    console.log('Update Scores:', scores);

    // Now you can use this parsed data to update your game state or render the changes
    // For example, call a function to update the canvas with the new positions
    //updateCanvas(racketPositions, ballPosition);
}

// Example usage
// parseUpdateData(newData);

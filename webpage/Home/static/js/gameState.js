// const canvas = document.getElementById('canvas');
// const ctx = canvas.getContext('2d');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');


// keyboard keys
let UP =     'up';
let DOWN =   'dn';
let LEFT =   'lf';
let RIGHT =  'rt';
let SPACE =  ' ';

// keypad keys
let KW = 'w';
let KS = 's';
let KA = 'a';
let KD = 'd';
let NZERO = '0';

let START = 'start_game';
let CLOSE = 'end_game';
let KEYPRESS = 'key_press';
let ESCAPE = None;
let RETURN = None;

    //get init_data from gameState.js

// Store the initial dimensions
const initialWidth = canvas.width;
const initialHeight = canvas.height;

// both bottom
// const initParam = {
//     'gameType': 'Ping',
//     'sizeInfo': {'width': 2048, 'height': 1024, 'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 'sRacket': 160, 'sBall': 20},
//     'racketCount': 2,
//     'racketInitPos': [682, 1004, 'x', 1365, 1004, 'x'],
//     'ballInitPos': [1024, 682],
//     'teamCount': 2
// };

// in front of each other
const initParam = {
     'gameType': 'Pong', 
     'sizeInfo': {'width': 2048, 'height': 1024, 
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 
        'sRacket': 160, 'sBall': 20}, 
    'racketCount': 2, 
    'racketInitPos': [20, 512, 'y', 2028, 512, 'y'], 
    'ballInitPos': [512, 512], 
    'teamCount': 2
};

// 4 players
// const initParam = {
//     'gameType': 'Pingest', 
//     'sizeInfo': {
//         'width': 1536, 'height': 1024, 
//         'wRatio': 0.0006510416666666666, 'hRatio': 0.0009765625, 
//         'sRacket': 160, 'sBall': 20}, 
//     'racketCount': 4, 
//     'racketInitPos': [438, 20, 'x', 1097, 20, 'x', 438, 1004, 'x', 1097, 1004, 'x'], 
//     'ballInitPos': [1152, 768],
//     'teamCount': 4
// }

// Afficher les valeurs dans la console
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

function setCanvasSize() {
    const parent = canvas.parentElement

    //Use initial dimensions if the parent is smaller
    canvas.width = Math.min(initialWidth, parent.clientWidth);
    canvas.height = Math.min(initialHeight, parent.clientHeight);
    
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}
setCanvasSize();



document.addEventListener("keydown", function (event) {
    //paddle1
    // Move paddle up (keyCode 38 or W key)
    if (event.key === "ArrowUp") {// && paddle1.y > 0) {
        console.log('ArrowUp');
        _send_player_keyevent(UP)
        //paddle1.y -= paddle1.speed;
    }
    
    // Move paddle down (keyCode 40 or S key)
    if (event.key === "ArrowDown") {// && paddle1.y < canvas.height - paddle1.height) {
        console.log('ArrowDown');
        _send_player_keyevent(DOWN)
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
        _send_player_keyevent(RIGHT)
        // paddle1.x += paddle1.speed;
    }
    
    // paddle2
    // Move paddle up (keyCode 38 or W key)
    if ( event.key === 'w') {// && paddle2.y > 0) {
        console.log('W');
        _send_player_keyevent(KW)
        // paddle2.y -= paddle2.speed;
    }
    
    // Move paddle down (keyCode 40 or S key)
    if ( event.key === 's') {// && paddle2.y < canvas.height - paddle2.height) {
        console.log('S');
        _send_player_keyevent(KS)
        // paddle2.y += paddle2.speed;
    }
    
    // Move paddle left (keyCode 37 or A key)
    if ( event.key === 'a') {// && paddle2.x > 0) {
        console.log('A');
        _send_player_keyevent(KA)
        // paddle2.x -= paddle2.speed;
    }
    
    // Move paddle right (keyCode 39 or D key)
    if ( event.key === 'd') {// && paddle2.x < canvas.width - paddle2.width) {
        console.log('D');
        _send_player_keyevent(KD)
        // paddle2.x += paddle2.speed;
    }
});

// 

// Afficher les valeurs dans la console
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

function setCanvasSize() {
    const parent = canvas.parentElement

    //Use initial dimensions if the parent is smaller
    canvas.width = Math.min(initialWidth, parent.clientWidth);
    canvas.height = Math.min(initialHeight, parent.clientHeight);
    
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}
setCanvasSize();


// start update system from any data first 
// Sample update data
const newData = {'gameID': 1, 'racketPos': [20, 512, 2028, 512], 'ballPos': [522, 522], 'lastPonger': 0, 'scores': [0, 0]};

// Function to parse update data
function parseUpdateData(update) {
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
    updateCanvas(racketPositions, ballPosition);
}

// Example usage
parseUpdateData(newData);

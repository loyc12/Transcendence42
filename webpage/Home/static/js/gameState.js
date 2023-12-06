// const canvas = document.getElementById('canvas');
// const ctx = canvas.getContext('2d');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

    //get init_data from gameState.js

// Store the initial dimensions
const initialWidth = canvas.width;
const initialHeight = canvas.height;

function setCanvasSize() {
    const parent = canvas.parentElement

    //Use initial dimensions if the parent is smaller
    canvas.width = Math.min(initialWidth, parent.clientWidth);
    canvas.height = Math.min(initialHeight, parent.clientHeight);
    
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}
setCanvasSize();

// Supposons que cela se passe dans un fichier (initParser.js)
const initParam = {
    'gameType': 'Ping',
    'sizeInfo': {'width': 2048, 'height': 1024, 'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 'sRacket': 160, 'sBall': 20},
    'racketCount': 2,
    'racketInitPos': [682, 1004, 'x', 1365, 1004, 'x'],
    'ballInitPos': [1024, 682],
    'teamCount': 2
};

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

















// document.addEventListener("keydown", function (event) {
//     //paddle1
//     // Move paddle up (keyCode 38 or W key)
//     if ((event.keyCode === 38) && paddle1.y > 0) {
//         paddle1.y -= paddle1.speed;
//     }
    
//     // Move paddle down (keyCode 40 or S key)
//     if ((event.keyCode === 40 ) && paddle1.y < canvas.height - paddle1.height) {
//         paddle1.y += paddle1.speed;
//     }

//     // Move paddle left (keyCode 37 or A key)
//     if ((event.keyCode === 37 ) && paddle1.x > 0) {
//         paddle1.x -= paddle1.speed;
//     }
    
//     // Move paddle right (keyCode 39 or D key)
//     if ((event.keyCode === 39 ) && paddle1.x < canvas.width - paddle1.width) {
//         paddle1.x += paddle1.speed;
//     }
    
//     // paddle2
//     // Move paddle up (keyCode 38 or W key)
//     if (( event.key === 'w') && paddle2.y > 0) {
//         paddle2.y -= paddle2.speed;
//     }
    
//     // Move paddle down (keyCode 40 or S key)
//     if (( event.key === 's') && paddle2.y < canvas.height - paddle2.height) {
//         paddle2.y += paddle2.speed;
//     }
    
//     // Move paddle left (keyCode 37 or A key)
//     if (( event.key === 'a') && paddle2.x > 0) {
//         paddle2.x -= paddle2.speed;
//     }
    
//     // Move paddle right (keyCode 39 or D key)
//     if (( event.key === 'd') && paddle2.x < canvas.width - paddle2.width) {
//         paddle2.x += paddle2.speed;
//     }
// });

// function update() {
//     // Clear the canvas
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     ctx.fillStyle = '#000000';
//     ctx.fillRect(0, 0, canvas.width, canvas.height);
    
//     // Check for collisions with the paddle
//     if (
//         ball.x + ball.radius > paddle1.x &&
//         ball.x - ball.radius < paddle1.x + paddle1.width &&
//         ball.y + ball.radius > paddle1.y &&
//         ball.y - ball.radius < paddle1.y + paddle1.height
//         ) {
//             ball.color = "#ff6700"; // Change to green color
//     } 
        
//         // Check for collisions with the paddle
//     if (
//         ball.x + ball.radius > paddle2.x &&
//         ball.x - ball.radius < paddle2.x + paddle2.width &&
//         ball.y + ball.radius > paddle2.y &&
//         ball.y - ball.radius < paddle2.y + paddle2.height
//         ) {
//             ball.color = "#23e301"; // Change to green color
//     }
                
//     // Draw the paddle
//     ctx.fillStyle = paddle1.color;
//     ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
    
//     ctx.fillStyle = paddle2.color;
//     ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);
    
//     ctx.font = "42px Arial";
//     ctx.fillStyle = "#ffffff";
//     ctx.fillText(s1, 100, 50);
//     ctx.fillText(s2, 700, 50);

    
    
//     // Draw the ball
//     ctx.fillStyle = ball.color;
//     ctx.beginPath();
//     ctx.arc(ball.x, ball.y, ball.radius, 0, 2 * Math.PI);
//     ctx.fill();


//     // Request the next animation frame
//     requestAnimationFrame(update);
// }
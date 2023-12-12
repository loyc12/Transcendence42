let score1 = 0;
let score2 = 0;

let setCurrentState = function (initData) {
    currentGameInfo = initData;
};

const players = [
    { name: 'Player 1', rank: 1 },
    { name: 'Player 2', rank: 2 },
    { name: 'Player 3', rank: 3 },
    { name: 'Player 4', rank: 4 },
];

// Function to get the player's color based on their rank
let getPlayerColor = function(rank) {
    // Use modulo operator to cycle through colors if there are more ranks than colors
    const index = rank % playerColors.length;
    return playerColors[index];
}

let getPlayerShadowColor = function(rank) {
    // Use modulo operator to cycle through colors if there are more ranks than colors
    const index = rank % playerColors.length;
    return playerShadowColors[index];
}


let clearCanvas = function (ctx, w, h) {
    ctx.clearRect(0, 0, w, h); // Clear the entire canvas
}

let renderCanvas = function (ctx, gameInfo) {
    // You can add additional rendering logic here
    // For now, let's just log the canvas dimensions
    
    // Render game elements based on initial game data
    renderBall(ctx, gameInfo, gameInfo.update);
    renderRackets(ctx, gameInfo, gameInfo.update);
    console.log(`Canvas Dimensions: ${canvas.width} x ${canvas.height}`);

    console.log('Game Score: S1:S2 :', gameInfo.update.scores);
    
    // ctx.font = "42px Arial";
    // ctx.fillStyle = "#ffffff";
    // ctx.fillText(gameInfo.update.scores[0], 100, 50);
    // ctx.fillText(gameInfo.update.scores[1], 700, 50);

}

let renderBall = function (ctx, gameInfo, update) {
    // console.log('gameInfo in renderBall : ' + gameInfo)

    const x = update.ballPos[0];
    const y = update.ballPos[1];
    const shadow = getPlayerShadowColor(update.lastPonger);
    ctx.fillStyle = 'red';// Ball color (customize as needed)
    ctx.beginPath();
    ctx.shadowBlur = 40;
    ctx.shadowColor = shadow;
    ctx.arc(x, y, gameInfo.ballSize * 0.5, 0, 2 * Math.PI); // Assuming ballRadius is defined
    ctx.fill();
}

let renderRackets = function(ctx, gameInfo, update) {
    let orientations = gameInfo.orientations;
    let racketCount = gameInfo.racketCount;
    let x, y, w, h;
    let color, shadow;

    for (let i = 0; i < racketCount; i++) {
        x = update.racketPos[2*i] + currentGameInfo.offsets[2*i];
        y = update.racketPos[2*i + 1] + currentGameInfo.offsets[2*i + 1];

        // Set the color of the racket based on the player's rank
        color = getPlayerColor(i);
        if (gameInfo.gameType === 'Pong' && i > 2) {
            color = '#ffffff';   }
        shadow = getPlayerShadowColor(i);
  
        // Check if the position of the racket is 'x'
        if (orientations[i] === 'x') {
            w = gameInfo.racketSize;
            h = gameInfo.ballSize;
        }
        else if (orientations[i] === 'y') {
            w = gameInfo.ballSize;
            h = gameInfo.racketSize;
        }
        
        ctx.fillStyle = color;
        ctx.shadowBlur = 40;
        ctx.shadowColor = shadow;
        ctx.fillRect(x, y, w, h);
    }
}


/// Should be the only function in the rendering chain to 
/// access global variables. Every downstream function call should take 
/// them as arguments.
let updateCanvas = function (gameInfo) {

    // Update the canvas based on the new data
    // Clear the canvas
    clearCanvas(ctx, canvas.width, canvas.height);
    // Render the canvas with the new data
    renderCanvas(ctx, gameInfo);
}

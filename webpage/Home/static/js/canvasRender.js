
let setCurrentState = function (initData) {
    currentGameInfo = initData;
};

const players = [
    { name: 'AI', rank: 0},
    { name: 'Player 1', rank: 1 },
    { name: 'Player 2', rank: 2 },
    { name: 'Player 3', rank: 3 },
    { name: 'Player 4', rank: 4 },
];

// Function to get the player's color based on their rank
//  Use modulo operator to cycle through colors if there are more ranks than colors
let getPlayerColor = function(rank) {
    const index = (rank + 1) % playerColors.length;
    return playerColors[index];
}

let getPlayerShadowColor = function(rank) {
    const index = (rank + 1) % playerColors.length;
    return playerShadowColors[index];
}

// Clear the entire canvas
let clearCanvas = function (ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
}

let renderCanvas = function (ctx, gameInfo) {

    // Score Pos
    let scorePlayer1 = [(canvas.width / 2 - 140 ) , 250];
    let scorePlayer2 = [(canvas.width / 2 + 100 ) , 250];
    let scorePlayer3 = [(canvas.width / 2 - 140 ) , (canvas.height - 250)];
    let scorePlayer4 = [(canvas.width / 2 + 100 ) , (canvas.height - 250)];

    // Render game elements based on initial game data
    renderBall(ctx, gameInfo, gameInfo.update);
    renderRackets(ctx, gameInfo, gameInfo.update);

    ctx.font = "64px Arial";
    ctx.fillStyle = "gray";
    ctx.fillRect(canvas.width / 2, 0, 1, canvas.height);
    ctx.fillStyle = "white";

    ctx.fillText(gameInfo.update.scores[0], scorePlayer1[0], scorePlayer1[1]);
    ctx.fillText(gameInfo.update.scores[1], scorePlayer2[0], scorePlayer2[1]);
    if (gameInfo.gameType === 'Pingest') {
        ctx.fillText(gameInfo.update.scores[2], scorePlayer3[0], scorePlayer3[1]);
        ctx.fillText(gameInfo.update.scores[3], scorePlayer4[0], scorePlayer4[1]);
    }
}

let renderBall = function (ctx, gameInfo, update) {
    const x = update.ballPos[0];
    const y = update.ballPos[1];
    let ballColorLast = getPlayerColor(update.lastPonger - 1);
    const shadow = getPlayerShadowColor(update.lastPonger - 1);
    ctx.beginPath();
    ctx.shadowBlur = 40;
    ctx.fillStyle = ballColorLast;
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
        shadow = getPlayerShadowColor(i);
        if (gameInfo.gameType === 'Pong' && i > 1) {
            color = '#ffffff'; 
            shadow = '#ffffff';  }

        if (orientations[i] === 'y' || gameInfo.gameType === 'Pong') {
            w = gameInfo.ballSize;
            h = gameInfo.racketSize;
        }
        else if (orientations[i] === 'x') {
            w = gameInfo.racketSize;
            h = gameInfo.ballSize;
        }

        ctx.fillStyle = color;
        ctx.shadowBlur = 40;
        ctx.shadowColor = shadow;
        ctx.fillRect(x, y, w, h);
    }
}

/// Should be the only function in the rendering chain to
/// access global variables. Every downstream function call should take them as arguments.
let updateCanvas = function (gameInfo) {
    // Update the canvas based on the new data
    clearCanvas(ctx, canvas.width, canvas.height);
    renderCanvas(ctx, gameInfo);
}

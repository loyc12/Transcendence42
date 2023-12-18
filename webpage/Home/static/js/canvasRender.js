// let sx = 0;
// let sy = 0;
// let scorePlayer1 = [(canvas.width / 2 - 50 ) , 250];
// let scorePlayer2 = [(canvas.width / 2 + 50 ) , 250];
// let scorePlayer3 = [(canvas.width / 2 - 50 ) , (canvas.height - 250)];
// let scorePlayer4 = [(canvas.width / 2 + 50 ) , (canvas.height - 250)];

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

    // Score Pos
    let scorePlayer1 = [(canvas.width / 2 - 140 ) , 250];
    let scorePlayer2 = [(canvas.width / 2 + 100 ) , 250];
    let scorePlayer3 = [(canvas.width / 2 - 100 ) , (canvas.height - 250)];
    let scorePlayer4 = [(canvas.width / 2 + 100 ) , (canvas.height - 250)];

    // Render game elements based on initial game data
    renderBall(ctx, gameInfo, gameInfo.update);
    renderRackets(ctx, gameInfo, gameInfo.update);

    ctx.font = "64px Arial";
    ctx.fillStyle = "gray";
    ctx.fillRect(canvas.width / 2, 0, 1, canvas.height);
    ctx.fillStyle = "white";
    // console.log("gameInfo : " + gameInfo);
    // console.log("gameInfo.update : " + gameInfo.update)
    // console.log("gameInfo.update.scores : " + gameInfo.update.scores);

    // ctx.fillText(gameInfo.update.scores, (canvas.width / 2 - 100) , 250);
    console.log('gameInfo.update.scores[0]  WIDTH: ' + canvas.width);
    console.log('gameInfo.update.scores[0]  HEIGHT: ' + canvas.height);
    console.log('gameInfo.update.scores[0]  POS: ' + scorePlayer1);
    console.log('gameInfo.update.scores[1]  POS: ' + scorePlayer2);
    // console.log('gameInfo.update.scores[2]  POS: ' + scorePlayer3);
    // console.log('gameInfo.update.scores[3]  POS: ' + scorePlayer4);

    // for (let i = 0; i < currentGameInfo.racketCount; i++) {
            ctx.fillText(gameInfo.update.scores[0], scorePlayer1[0], scorePlayer1[1]);
            ctx.fillText(gameInfo.update.scores[1], scorePlayer2[0], scorePlayer2[1]);
    //     const scoreElement = document.createElement('div');
    //     scoreElement.textContent = `Player ${i + 1} Score: ${gameInfo.update.scores[i]}`;
    //     gameInfoContainer.appendChild(scoreElement);
    // }

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
        // console.log('racket pos' + update.racketPos[2*i + 1] + 'racket offset ' + currentGameInfo.offsets[2*i + 1]);
        // console.log('racketCount : '+ i + ' de ' + racketCount + ' >> ' + x + ' : ' + y);
        console.log('racketCheck : X >> '+ update.racketPos[2*i] + ' : Y >> ' + update.racketPos[2*i + 1] );

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


// let initStart = true;

// let currentGameInfo = null;
// let currentUpdate = null;


let setCurrentState = function (initData) {//update) {
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

// Example usage:
players.forEach(player => {
    const playerName = player.name;
    const playerRank = player.rank;
    const playerColor = getPlayerColor(playerRank);

    console.log(`${playerName} (Rank ${playerRank}): Color - ${playerColor}`);
    // Now you can use playerColor to set the color in your rendering logic
});

let clearCanvas = function (ctx, w, h) {
    ctx.clearRect(0, 0, w, h); // Clear the entire canvas
}

let renderCanvas = function (ctx, gameInfo) {
    // const { width, height } = gameInfo.sizeInfo;
    // const { bx, by } = gameInfo.ballInitPos;

    // console.log('gameInfo in renderCanvas : ' + gameInfo)
    // Set canvas dimensions (ALREADY DONE IN parseInitData() ... maybe)
    // canvas.width = width;
    // canvas.height = height;

    // Render black background (ALREADY DONE PRIOR)
    // clearCanvas()

    // You can add additional rendering logic here
    // For now, let's just log the canvas dimensions
    
    // Render game elements based on initial game data
    renderBall(ctx, gameInfo, gameInfo.update);
    renderRackets(ctx, gameInfo, gameInfo.update);
    // console.log(`Canvas Dimensions: ${canvas.width} x ${canvas.height}`);
}

let renderBall = function (ctx, gameInfo, update) {
    // console.log('gameInfo in renderBall : ' + gameInfo)

    const x = update.ballPos[0] + gameInfo.ballOffset;//(ballPos[0] + gameInfo.ballOffset) * gameInfo.xRatio;
    const y = update.ballPos[1] + gameInfo.ballOffset;// * gameInfo.yRatio;
    const shadow = getPlayerShadowColor(update.lastPonger);
    ctx.fillStyle = 'red'; // Ball color (customize as needed)
    ctx.beginPath();
    //ctx.arc(initParam.ballInitPos[0], initParam.ballInitPos[1], initParam.sizeInfo.sBall, 0, 2 * Math.PI); // Assuming ballRadius is defined
    ctx.shadowBlur = 40;
    ctx.shadowColor = shadow;
    ctx.arc(x, y, gameInfo.ballSize, 0, 2 * Math.PI); // Assuming ballRadius is defined
    ctx.fill();
}

let renderRackets = function(ctx, gameInfo, update) {
    // let tot = 0;
    // console.log('gameInfo in renderRackets : ' + gameInfo)
    let orientations = gameInfo.orientations;
    let racketCount = gameInfo.racketCount;
    let x, y, w, h;
    let color, shadow;

    for (let i = 0; i < racketCount; i++) {
        // x = (racketPositions[2*i] + gameInfo.offsets[2*i]) * gameInfo.xRatio;
        x = update.racketPos[2*i] + currentGameInfo.offsets[2*i];
        y = update.racketPos[2*i + 1] + currentGameInfo.offsets[2*i + 1];
        // y = (racketPositions[2*i + 1] + gameInfo.offsets[2*i + 1]) * gameInfo.yRatio;
        // console.log('racket ' + i + ': (' + x + ', ' + y + ')')
        // Set the color of the racket based on the player's rank
        color = getPlayerColor(i);
        shadow = getPlayerShadowColor(i);
        
        // ctx[0].fillStyle = "white";
        // ctx[0].fillRect(0,0,200,200);
        // ctx[0].shadowBlur = 20;
        // ctx[0].shadowColor = "black";
        // ctx[0].fillRect(50,50,100,100);

        //ctx.fillStyle = 'red';//getPlayerColor(i);
        // Check if the position of the racket is 'x'
        if (orientations[i] === 'x') {
            // console.log(`orientation horizontal :: racket box (${x}, ${y}) (${x + gameInfo.racketSize}, ${y + gameInfo.ballSize})`)
            w = gameInfo.racketSize;
            h = gameInfo.ballSize;
            //ctx.fillRect(x, y, gameInfo.racketSize, gameInfo.ballSize); // Assuming racketWidth and racketHeight are defined
        }
        // else if (initParam.racketInitPos[i + 2] === 'y'){
        else if (orientations[i] === 'y') {
            // console.log(`orientation vertical :: racket box (${x}, ${y}) (${x + gameInfo.racketSize}, ${y + gameInfo.ballSize})`)
            w = gameInfo.ballSize;
            h = gameInfo.racketSize;
            // ctx.fillRect(x, y, gameInfo.ballSize, gameInfo.racketSize); // Assuming racketWidth and racketHeight are defined
        }
        ctx.fillStyle = color;
        ctx.shadowBlur = 40;
        ctx.shadowColor = shadow;
        ctx.fillRect(x, y, w, h);
    }
    
    // let tot = 0;
    // for (let i = 0; i < initParam.racketInitPos.length; i += 3) {
    //     tot += 1;
    //     let racketX = initParam.racketInitPos[i];
    //     let racketY = initParam.racketInitPos[i + 1];
    //     console.log(racketX);
    //     console.log(racketY);
    //     console.log("player :", tot);
    //     // Set the color of the racket based on the player's rank
    //     ctx.fillStyle = getPlayerColor(tot);
    //     // Check if the position of the racket is 'x'
    //     if (initParam.racketInitPos[i + 2] === 'x') {
    //         ctx.fillRect(racketX, racketY, initParam.sizeInfo.sRacket, initParam.sizeInfo.sBall); // Assuming racketWidth and racketHeight are defined
    //     }
    //     else if (initParam.racketInitPos[i + 2] === 'y'){
    //         ctx.fillRect(racketX, racketY,  initParam.sizeInfo.sBall, initParam.sizeInfo.sRacket); // Assuming racketWidth and racketHeight are defined
    //     }
    //     else {
    //         // Render the racket at the specified position
    //         ctx.fillStyle = 'yellow'; // Racket color (customize as needed)
    //         ctx.fillRect(racketX, racketY, initParam.sizeInfo.sBall, initParam.sizeInfo.sBall); // Assuming racketWidth and racketHeight are defined
    //     }
    // }
}


/// Should be the only function in the rendering chain to 
/// access global variables. Every downstream function call should take 
/// them as arguments.

// let updateCanvas = function (gameInfo) {
let updateCanvas = function (gameInfo) {

    // Update the canvas based on the new data
    // console.log('Updating canvas with new data:', gameInfo);
    // Clear the canvas
    clearCanvas(ctx, canvas.width, canvas.height);
    // Render the canvas with the new data
    renderCanvas(ctx, gameInfo);
}


//
// // Assume jsonData is the JSON response from your server
// const jsonData = '{"gameID": 1, "racketPos": [20, 512, 2028, 512], "ballPos": [522, 522], "lastPonger": 0, "scores": [0, 0]}';

// // Parse JSON data
// const parsedData = JSON.parse(jsonData);

// // Render the game with parsed data
// renderGame(parsedData);
//
// // Assume jsonData is the JSON response from your server
// const jsonData = '{"gameID": 1, "racketPos": [20, 512, 2028, 512], "ballPos": [522, 522], "lastPonger": 0, "scores": [0, 0]}';

// // Parse JSON data
// const parsedData = JSON.parse(jsonData);

// // Render the game with parsed data
// renderGame(parsedData);

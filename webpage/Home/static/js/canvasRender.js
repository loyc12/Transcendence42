
// let initStart = true;

// let currentGameInfo = null;
// let currentUpdate = null;


let setCurrentState = function (initData) {//update) {
    currentGameInfo = initData;

    // updateCanvas = update
    // console.log('parseUpdateData : ' + update)
    
    // const gameId = update.gameID;
    // const racketPositions = update.racketPos;
    // const ballPosition = update.ballPos;
    // const lastPonger = update.lastPonger;
    // const scores = update.scores;

    // currentGameInfo = {
    //     'gameType': update.gameType,
    //     'sizeInfo': {
    //         'width': 2048, 'height': 1024, 
    //         'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 
    //         'sRacket': 160, 'sBall': 20
    //         // 'sRacket': 160, 'sBall': 20
    //     },
    //     'racketCount': 2,
    //     'teamCount': 2,
    //     'orientations': ['y', 'y'],
    //     'update': {
    //         'racketPos': [682, 1004, 1365, 1004 ],
    //         'ballPos': [1024, 682],
    //         'score' : [0, 0],
    //     }
    // }
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

// class RenderModule {
//     constructor(initData) {
//         this.initData = initData;
//     }
//     render() {
//         // Utilisez les données du initData pour effectuer le rendu
//         console.log('Rendering with Width:', this.initData.sizeInfo.width);
//         console.log('Rendering with Height:', this.initData.sizeInfo.height);
//     }
// }


// Utilisation du module de rendu

// if (initStart) {
//     const renderModule = new RenderModule(initParam);
//     const initWidth = initParam.sizeInfo.width;
//     const initHeight = initParam.sizeInfo.height;
//     // console.log(initParam);
//     console.log("init_dataValue width :", initParam.sizeInfo.width);
//     console.log("init_dataValue height:", initParam.sizeInfo.height);
//     renderModule.render();
//     initStart = false;
// }

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
        // else {
        //     // Render the racket at the specified position
        //     ctx.fillStyle = 'yellow'; // Racket color (customize as needed)
        //     ctx.fillRect(x, y, gameInfo.ballSize, gameInfo.ballSize); // Assuming racketWidth and racketHeight are defined
        // }
        
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


// class UpdateGame {
    //     constructor(canvasId, gameData) {
    //         this.canvas = document.getElementById(canvasId);
    //         this.ctx = this.canvas.getContext('2d');
    //         this.gameData = gameData;

    //        // Get initial game data from data attributes console.log
    //        this.gameData = {
    //             'sizeInfo': {
    //                 'width': parseInt(this.canvas.getAttribute('data-width')),
    //                 'height': parseInt(this.canvas.getAttribute('data-height')),
    //                 'sRacket': parseInt(this.canvas.getAttribute('data-sRacket')),
    //                 'sBall': parseInt(this.canvas.getAttribute('data-sBall'))
    //             },
    //         // Add more initial data if needed
    //     };

    //     // Log initial data to console
    //     console.log('Initial Game Data:', this.gameData);

    //     // Set up initial game state
    //     this.initState();
//     }

//     initState() {
    //         // Clear the canvas
    //         this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    //         // Render game elements based on initial game data
    //         this.renderRackets();
    //         this.renderBall();
    //         // Add more rendering functions based on your game design
    //     }

//     renderRackets() {
    //         const racketCount = this.gameData.racketCount;
    //         const racketInitPos = this.gameData.racketInitPos;

    //         // Render rackets based on the initial positions
    //         for (let i = 0; i < racketCount; i++) {
    //             const xPos = racketInitPos[i * 3];
    //             const yPos = racketInitPos[i * 3 + 1];
    //             const racketWidth = this.gameData.sizeInfo.sRacket;
    //             const racketHeight = 10;  // You can adjust the height

    //             this.ctx.fillRect(xPos, yPos, racketWidth, racketHeight);
    //         }
    //     }

//        renderBall() {
    //         const ballInitPos = this.gameData.ballInitPos;
    //         const ballSize = this.gameData.sizeInfo.sBall;

    //         console.log(ballInitPos[0]);
    //         console.log(ballInitPos[1]);

    //         // Render the ball based on the initial position
    //         this.ctx.beginPath();
    //         this.ctx.arc(ballInitPos[0], ballInitPos[1], ballSize, 0, 2 * Math.PI);
    //         this.ctx.fill();
    //     }

//     updateGameData(newGameData) {
    //         // Update game data based on the received data
    //         Object.assign(this.gameData, newGameData);

    //         // Log updated game data to console
    //         console.log('Updated Game Data:', this.gameData);

    //         // update game state based on the updated game data
    //         this.initState();
//     }
// }






// // Create an instance of CanvasRender using the gameState.initData
// const canvasRender = new CanvasRender('gameCanvas', gameState.initData);

// class UpdateGame {
//     constructor(canvasId, gameData) {
//         this.canvas = document.getElementById(canvasId);
//         this.ctx = this.canvas.getContext('2d');
//         this.gameData = gameData;

//        // Get initial game data from data attributes console.log
//        this.gameData = {
//             'sizeInfo': {
//                 'width': parseInt(this.canvas.getAttribute('data-width')),
//                 'height': parseInt(this.canvas.getAttribute('data-height')),
//                 'sRacket': parseInt(this.canvas.getAttribute('data-sRacket')),
//                 'sBall': parseInt(this.canvas.getAttribute('data-sBall'))
//             },
//         // Add more initial data if needed
//     };

//     // Log initial data to console
//     console.log('Initial Game Data:', this.gameData);

//     // Set up initial game state
//     this.initState();
//     }

//     initState() {
//         // Clear the canvas
//         this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

//         // Render game elements based on initial game data
//         this.renderRackets();
//         this.renderBall();
//         // Add more rendering functions based on your game design
//     }

//     renderRackets() {
//         const racketCount = this.gameData.racketCount;
//         const racketInitPos = this.gameData.racketInitPos;

//         // Render rackets based on the initial positions
//         for (let i = 0; i < racketCount; i++) {
//             const xPos = racketInitPos[i * 3];
//             const yPos = racketInitPos[i * 3 + 1];
//             const racketWidth = this.gameData.sizeInfo.sRacket;
//             const racketHeight = 10;  // You can adjust the height

//             this.ctx.fillRect(xPos, yPos, racketWidth, racketHeight);
//         }
//     }

//     renderBall() {
//         const ballInitPos = this.gameData.ballInitPos;
//         const ballSize = this.gameData.sizeInfo.sBall;

//         console.log(ballInitPos[0]);
//         console.log(ballInitPos[1]);

//         // Render the ball based on the initial position
//         this.ctx.beginPath();
//         this.ctx.arc(ballInitPos[0], ballInitPos[1], ballSize, 0, 2 * Math.PI);
//         this.ctx.fill();
//     }

//     updateGameData(newGameData) {
//         // Update game data based on the received data
//         Object.assign(this.gameData, newGameData);

//         // Log updated game data to console
//         console.log('Updated Game Data:', this.gameData);

//         // update game state based on the updated game data
//         this.initState();
//     }
// }



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

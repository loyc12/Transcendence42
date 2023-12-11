
let initStart = true;
const playerColors = ['#ff10f0', '#23e301', '#04d9ff', '#ff6700'];

// let currentGameInfo = null;
// let currentUpdate = null;


let setCurrentState = function (initData) {//update) {

    // updateCanvas = update
    // console.log('parseUpdateData : ' + update)
    
    // const gameId = update.gameID;
    // const racketPositions = update.racketPos;
    // const ballPosition = update.ballPos;
    // const lastPonger = update.lastPonger;
    // const scores = update.scores;

    console.log('setCurrentState thgameType:', initData.gameType);
    currentGameInfo = initData;
    // currentGameInfo = {
    //     'gameType': update.gameType,
    //     'sizeInfo': {
    //         'width': 2048, 'height': 1024, 
    //         'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 
    //         'rSize': 160, 'bSize': 20
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
    const index = (rank - 1) % playerColors.length;
    return playerColors[index];
}

// Example usage:
players.forEach(player => {
    const playerName = player.name;
    const playerRank = player.rank;
    const playerColor = getPlayerColor(playerRank);

    console.log(`${playerName} (Rank ${playerRank}): Color - ${playerColor}`);
    // Now you can use playerColor to set the color in your rendering logic
});

class RenderModule {
    constructor(initData) {
        this.initData = initData;
    }
    render() {
        // Utilisez les données du initData pour effectuer le rendu
        console.log('Rendering with Width:', this.initData.sizeInfo.width);
        console.log('Rendering with Height:', this.initData.sizeInfo.height);
    }
}


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

let renderCanvas = function (gameInfo) {
    const { width, height } = gameInfo.sizeInfo;
    // const { bx, by } = gameInfo.ballInitPos;

    console.log('gameInfo in renderCanvas gameType: ' + gameInfo.gameType);
    console.log('gameInfo in renderCanvas width: ' + gameInfo.sizeInfo.width);
    console.log('gameInfo in renderCanvas height: ' + gameInfo.sizeInfo.height);
    // Set canvas dimensions
    canvas.width = width;
    canvas.height = height;

    // Render black background
    clearCanvas()
    // ctx.fillStyle = 'black';
    // ctx.fillRect(0, 0, width, height);


    // You can add additional rendering logic here
    // For now, let's just log the canvas dimensions
    
    // Render game elements based on initial game data
    renderBall(ctx, gameInfo, gameInfo.update.ballPos);
    renderRackets(ctx, gameInfo, gameInfo.update.racketPos);
    console.log(`Canvas Dimensions: ${canvas.width} x ${canvas.height}`);
}

let renderBall = function (ctx, gameInfo, ballPos) {

    console.log('gameInfo in renderBall : ' + gameInfo)

    let x = (ballPos[0] + gameInfo.ballOffset) * gameInfo.xRatio;
    let y = (ballPos[1] + gameInfo.ballOffset) * gameInfo.yRatio;

    ctx.fillStyle = 'red'; // Ball color (customize as needed)
    ctx.beginPath();
    //ctx.arc(initParam.ballInitPos[0], initParam.ballInitPos[1], initParam.sizeInfo.sBall, 0, 2 * Math.PI); // Assuming ballRadius is defined
    ctx.arc(x, y, gameInfo.ballSize, 0, 2 * Math.PI); // Assuming ballRadius is defined
    ctx.fill();
}

let renderRackets = function(ctx, gameInfo, racketPositions) {
    
    // let tot = 0;
    console.log('gameInfo in renderRackets : ' + gameInfo)
    let orientations = gameInfo.orientations;
    let racketCount = gameInfo.racketCount;
    let x, y;

    for (let i = 0; i < racketCount; i++) {
        x = (racketPositions[2*i] + gameInfo.offsets[2*i]) * gameInfo.xRatio;
        y = (racketPositions[2*i + 1] + gameInfo.offsets[2*i + 1]) * gameInfo.yRatio;
        
        // Set the color of the racket based on the player's rank
        ctx.fillStyle = getPlayerColor(i);
        // Check if the position of the racket is 'x'
        if (orientations[i] === 'x') {
            console.log('x');
            ctx.fillRect(x, y, gameInfo.racketSize, gameInfo.ballSize); // Assuming racketWidth and racketHeight are defined
        }
        // else if (initParam.racketInitPos[i + 2] === 'y'){
        else if (orientations[i] === 'y') {
            console.log('y');
            ctx.fillRect(x, y,  gameInfo.ballSize, gameInfo.racketSize); // Assuming racketWidth and racketHeight are defined
        }
        else {
            // Render the racket at the specified position
            ctx.fillStyle = 'yellow'; // Racket color (customize as needed)
            ctx.fillRect(x, y, gameInfo.ballSize, gameInfo.ballSize); // Assuming racketWidth and racketHeight are defined
        }
    }
    /// 

}

let clearCanvas = function () {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the entire canvas
}


let updateCanvas = function (newData) {

    // Update the canvas based on the new data
    console.log('Updating canvas with new data:', newData);
    // Clear the canvas
    clearCanvas();
    // Render the canvas with the new data
    renderCanvas(newData);
}



/// viens de render_racket
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

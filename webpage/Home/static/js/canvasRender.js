class RenderModule {
    constructor(initData) {
        this.initData = initData;
    }

    render() {
        // Utilisez les données du initData pour effectuer le rendu
        console.log('Rendering with Width:', this.initData.sizeInfo.width);
        console.log('Rendering with Height:', this.initData.sizeInfo.height);
        // ... Ajoutez d'autres actions de rendu au besoin
    }
}

// Utilisation du module de rendu
const renderModule = new RenderModule(initParam);
renderModule.render();



// class CanvasRender {
//     constructor(canvasId, initState) {
//         this.canvas = document.getElementById(canvasId);
//         this.ctx = this.canvas.getContext('2d');
//         this.initState = initState;

//         // Render the initial state
//         this.render();
//     }

//     render() {
//         // Access this.initState.width, this.initState.height, etc., to render on the canvas
//         // Example:
//         this.ctx.fillStyle = 'blue';
//         this.ctx.fillRect(0, 0, this.initState.width, this.initState.height);
//     }
// }

// // Create an instance of CanvasRender using the gameState.initData
// const canvasRender = new CanvasRender('gameCanvas', gameState.initData);

// class PingGame {
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

// // // Example usage
// const gameData = {
//     'gameType': 'Ping',
//     'sizeInfo': {'width': 2048, 'height': 1024, 'wRatio': 0.00048828125, 'hRatio': 0.0009765625, 'sRacket': 160, 'sBall': 20},
//     'racketCount': 2,
//     'racketInitPos': [682, 1004, 'x', 1365, 1004, 'x'],
//     'ballInitPos': [1024, 682],
//     'teamCount': 2
// };

// // Example usage
// const pingGame = new PingGame('pingCanvas');

// // Simulate receiving new game data from the backend
// const newGameData = {
//     'sizeInfo': {
//         'width': 1200,
//         'height': 800,
//         'sRacket': 100,
//         'sBall': 15
//     },
//     // Add more updated data if needed
// };
// pingGame.updateGameData(newGameData);


//
// // Assume jsonData is the JSON response from your server
// const jsonData = '{"gameID": 1, "racketPos": [20, 512, 2028, 512], "ballPos": [522, 522], "lastPonger": 0, "scores": [0, 0]}';

// // Parse JSON data
// const parsedData = JSON.parse(jsonData);

// // Render the game with parsed data
// renderGame(parsedData);

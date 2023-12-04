// Get the canvas element
const canvas = document.getElementById("canvasGame");
const ctx = canvas.getContext("2d");

// Get the game info container
const gameInfoContainer = document.getElementById('game-info-container');

// Game state object
const gameState = {
    gameID: 0,
    racketPos: [],
    ballPos: [],
    score: []
};

// // Fake function to simulate an update or initial state
// function getFakeData() {
    //     return {
    //         gameID: 1,
    //         racketPos: ["canvas.width / 2 - 25", "50", "50", "canvas.height / 2 - 25", "canvas.width / 2 - 25", "canvas.height - 50", "canevas.width - 50", "canvas.height / 2 - 25"],
    //         ballPos: ["canvas.width / 2", "canvas.height / 2"],
    //         score: ["s1", "s2", "s3", "s4"]
//     };
// }

// Function to simulate fetching batch data from an external JSON file
async function fakeFetchBatchData() {
    try {
        const response = await fetch('data.json'); // Adjust the path accordingly

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching batch data:', error);
        // Handle the error as needed (e.g., display an error message, retry, etc.)
        return [];
    }
}

// // Update loop
// async function update() {
//     try {
//         // Fetch updated game state from the server (replace with your server URL)
//         // For testing purposes, use the fake function instead of fetch
//         const updatedGameState = getFakeData();

//         // Update game state
//         updateGameState(updatedGameState);

//         // Update HTML based on the game state
//         updateHTML();
//     } catch (error) {
//         console.error('Error fetching data:', error);
//         // Handle the error as needed (e.g., display an error message, retry, etc.)
//     } finally {
//         // Request the next animation frame
//         requestAnimationFrame(update);
//     }
// }

// Update loop
async function update() {
    try {
        // Fetch updated game state from the server (replace with your server URL)
        // For testing purposes, use the fake function instead of fetch
        const batchData = await fakeFetchBatchData();

        // Process batch data
        for (const updatedGameState of batchData) {
            updateGameState(updatedGameState);

            // Update HTML based on the game state
            updateHTML();

            // Delay for a short period to simulate time between updates
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    } catch (error) {
        console.error('Error fetching batch data:', error);
        // Handle the error as needed (e.g., display an error message, retry, etc.)
    } finally {
        // Request the next animation frame
        requestAnimationFrame(update);
    }
}

function updateGameState(updatedGameState) {
    // Update game state based on the received data
    gameState.gameID = updatedGameState.gameID;
    gameState.racketPos = updatedGameState.racketPos;
    gameState.ballPos = updatedGameState.ballPos;
    gameState.score = updatedGameState.score;
}

function updateHTML() {
    // Clear previous content
    gameInfoContainer.innerHTML = '';

    // Display game information
    const gameInfoElement = document.createElement('div');
    gameInfoElement.textContent = `Game ID: ${gameState.gameID}`;
    gameInfoContainer.appendChild(gameInfoElement);

    // Display racket positions
    for (let i = 0; i < gameState.racketPos.length; i += 2) {
        const racketElement = document.createElement('div');
        racketElement.textContent = `Racket ${i / 2 + 1}: (${gameState.racketPos[i]}, ${gameState.racketPos[i + 1]})`;
        gameInfoContainer.appendChild(racketElement);
    }

    // Display ball position
    const ballElement = document.createElement('div');
    ballElement.textContent = `Ball Position: (${gameState.ballPos[0]}, ${gameState.ballPos[1]})`;
    gameInfoContainer.appendChild(ballElement);

    // Display scores
    for (let i = 0; i < gameState.score.length; i++) {
        const scoreElement = document.createElement('div');
        scoreElement.textContent = `Player ${i + 1} Score: ${gameState.score[i]}`;
        gameInfoContainer.appendChild(scoreElement);
    }
    // Draw the ball
    ctx.fillStyle = ball.color;
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, 2 * Math.PI);
    ctx.fill();
}

// Start the update loop
update();

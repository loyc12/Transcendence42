// Get the game info container
const gameInfoContainer = document.getElementById('game-info-container');

// Game state object
const gameState = {
    gameID: 0,
    racketPos: [],
    ballPos: [],
    score: []
};

// Function to simulate an update or initial state
function getFakeData() {
    return {
        gameID: 1,
        racketPos: ["50", "canvas.height / 2 - 25", "canevas.width - 50", "canvas.height / 2 - 25"],
        ballPos: ["canvas.width / 2", "canvas.height / 2"],
        score: ["s1", "s2"]
    };
}

// Update loop
function update() {
    try {
        // Fetch updated game state from the server (replace with your server URL)
        // For testing purposes, use the fake function instead of fetch
        const updatedGameState = getFakeData();

        // Update game state
        updateGameState(updatedGameState);

        // Update HTML based on the game state
        updateHTML();
    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        // Request the next animation frame
        // requestAnimationFrame(update);
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

    // Display game information for each frame
    gameState.forEach((frame, index) => {
        const gameInfoElement = document.createElement('div');
        gameInfoElement.textContent = `Frame ${index + 1} - Game ID: ${frame.gameID}`;
        gameInfoContainer.appendChild(gameInfoElement);

        // Display racket positions
        for (let i = 0; i < frame.racketPos.length; i += 2) {
            const racketElement = document.createElement('div');
            racketElement.textContent = `Racket ${i / 2 + 1}: (${frame.racketPos[i]}, ${frame.racketPos[i + 1]})`;
            gameInfoContainer.appendChild(racketElement);
        }

        // Display ball position
        const ballElement = document.createElement('div');
        ballElement.textContent = `Ball Position: (${frame.ballPos[0]}, ${frame.ballPos[1]})`;
        gameInfoContainer.appendChild(ballElement);

        // Display scores
        for (let i = 0; i < frame.score.length; i++) {
            const scoreElement = document.createElement('div');
            scoreElement.textContent = `Player ${i + 1} Score: ${frame.score[i]}`;
            gameInfoContainer.appendChild(scoreElement);
        }

        // Draw the ball for each frame
        ctx.fillStyle = ball.color;
        ctx.beginPath();
        ctx.arc(frame.ballPos[0], frame.ballPos[1], ball.radius, 0, 2 * Math.PI);
        ctx.fill();
    });

    // Request the next animation frame
    // requestAnimationFrame(update);
}

// Start the update loop
update();
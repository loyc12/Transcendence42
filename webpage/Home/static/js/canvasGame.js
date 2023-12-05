 

    const ctx = document.getElementById('canvasGame').getContext('2d');

        ctx.font = '48px Nunito';
        // ctx.fillStyle = '#000000';
        // ctx.fillRect(0, 0, 800, 600);
        // ctx.fillStyle = '#FF10F0';
        // ctx.fillText('Game init...', 20, 50);
        
        // Create a paddle object
        var paddle1 = {
            x: canvas.width / 2 - 25,
            y:  50, // Center the paddle vertically
            width: 50,
            height: 10,
            color: "#ff10f0", // player1 color
            speed: 10
        };
        
        // Create a paddle object
        var paddle2 = {
            x: 50,
            y: canvas.height / 2 - 25, // Center the paddle vertically
            width: 10,
            height: 50,
            color: "#23e301", // Player2 color
            speed: 10
        };
        
        // Create a paddle object
        var paddle3 = {
            x: canvas.width / 2 - 25,
            y: canvas.height - 50, // Center the paddle vertically
            width: 50,
            height: 10,
            color: "#04d9ff", // Player3 color
            speed: 10
        };
        
        var paddle4 = {
            x: canvas.width - 50,
            y:  canvas.height / 2 - 25,
            width: 10,
            height: 50,
            color: "#ff6700", // player1 color
            speed: 10
        };

        
        // Create a ball object
        var ball = {
            x: canvas.width / 2,
            y: canvas.height / 2,
            radius: 5,
            color: "#0000ff", // Blue color
            speedX: 4,
            speedY: 4
        };

    // Listen to keyboard input
    document.addEventListener("keydown", function (event) {
        //paddle1
        // Move paddle up (keyCode 38 or W key)
        if ((event === "ArrowDown") && paddle1.y > 0) {
            paddle1.y -= paddle1.speed;
        }
        
        // Move paddle down (keyCode 40 or S key)
        if ((event === "ArrowUp" ) && paddle1.y < canvas.height - paddle1.height) {
            paddle1.y += paddle1.speed;
        }

        // Move paddle left (keyCode 37 or A key)
        if ((event === "ArrowLeft" ) && paddle1.x > 0) {
            paddle1.x -= paddle1.speed;
        }
        
        // Move paddle right (keyCode 39 or D key)
        if ((event === "ArrowRight" ) && paddle1.x < canvas.width - paddle1.width) {
            paddle1.x += paddle1.speed;
        }
        
        // paddle2
        // Move paddle up (keyCode 38 or W key)
        if (( event.key === 'w') && paddle2.y > 0) {
            paddle2.y -= paddle2.speed;
        }
        
        // Move paddle down (keyCode 40 or S key)
        if (( event.key === 's') && paddle2.y < canvas.height - paddle2.height) {
            paddle2.y += paddle2.speed;
        }
        
        // Move paddle left (keyCode 37 or A key)
        if (( event.key === 'a') && paddle2.x > 0) {
            paddle2.x -= paddle2.speed;
        }
        
        // Move paddle right (keyCode 39 or D key)
        if (( event.key === 'd') && paddle2.x < canvas.width - paddle2.width) {
            paddle2.x += paddle2.speed;
        }
        
        /// paddle3
        // Move paddle up (keyCode 38 or W key)
        if (( event.key === 'p') && paddle4.y > 0) {
            paddle4.y -= paddle4.speed;
        }
        
        // Move paddle down (keyCode 40 or S key)
        if (( event.key === ';') && paddle4.y < canvas.height - paddle4.height) {
            paddle4.y += paddle4.speed;
        }
        
        // Move paddle left (keyCode 37 or A key)
        if (( event.key === ',') && paddle3.x > 0) {
            paddle3.x -= paddle3.speed;
        }
        
        // Move paddle right (keyCode 39 or D key)
        if (( event.key === '.') && paddle3.x < canvas.width - paddle3.width) {
            paddle3.x += paddle3.speed;
        }
    });
    
    // Update loop
    function updateColor() {
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Update the ball position
        // ball.x += ball.speedX;
        // ball.y += ball.speedY;
        
        
        // Bounce the ball off the walls
        if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
            ball.speedX = -ball.speedX;
        }
        
        if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
            ball.speedY = -ball.speedY;
        }

        // Check for collisions with the paddle1
        if (
            ball.x + ball.radius > paddle1.x &&
            ball.x - ball.radius < paddle1.x + paddle1.width &&
            ball.y + ball.radius > paddle1.y &&
            ball.y - ball.radius < paddle1.y + paddle1.height
            ) {
            ball.color = "#ff10f0"; // Change to green color
        } 
            
        // Check for collisions with the paddle2
        if (
            ball.x + ball.radius > paddle2.x &&
            ball.x - ball.radius < paddle2.x + paddle2.width &&
            ball.y + ball.radius > paddle2.y &&
            ball.y - ball.radius < paddle2.y + paddle2.height
            ) {
            ball.color = "#23e301"; // Change to green color
        }
                
        // Check for collisions with the paddle3
        if (
            ball.x + ball.radius > paddle3.x &&
            ball.x - ball.radius < paddle3.x + paddle3.width &&
            ball.y + ball.radius > paddle3.y &&
            ball.y - ball.radius < paddle3.y + paddle3.height
            ) {
                ball.color = "#04d9ff"; // Change to green color
            }
                    
        // Check for collisions with the paddle4
        if (
            ball.x + ball.radius > paddle4.x &&
            ball.x - ball.radius < paddle4.x + paddle4.width &&
            ball.y + ball.radius > paddle4.y &&
            ball.y - ball.radius < paddle4.y + paddle4.height
            ) {
            ball.color = "#ff6700"; // Change to green color
        } 
                        
        // Draw the paddle
        ctx.fillStyle = paddle1.color;
        ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
        
        ctx.fillStyle = paddle2.color;
        ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);
        
        ctx.fillStyle = paddle3.color;
        ctx.fillRect(paddle3.x, paddle3.y, paddle3.width, paddle3.height);
        
        ctx.fillStyle = paddle4.color;
        ctx.fillRect(paddle4.x, paddle4.y, paddle4.width, paddle4.height);
        
        
        // Draw the ball
        ctx.fillStyle = ball.color;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, 2 * Math.PI);
        ctx.fill();

        // Request the next animation frame
        requestAnimationFrame(update);
    }
    
    // Start the update loop
    updateColor();

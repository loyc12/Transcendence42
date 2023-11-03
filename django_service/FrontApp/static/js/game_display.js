// set paddle position
var paddle1_y = 40;
var paddle2_y = 40;

// set paddle size
var paddle_thickness = 10;
var paddle_height = 100;

// set ball position
var ball_x = 50;
var ball_y = 50;

// set ball size
var ball_dimension = 6;

// set speed variables
var x_velocity = 5;
var y_velocity = x_velocity;
var computer_speed = 3;

// create variables to hold the player scores
var player1_score = 0;
var player2_score = 0;

// Set the score that wins
var winning_score = 5;
var reset_game = false;

window.onload = function ()  {
		// Wait for the page to finish loading
	
		// Retrieve and load the canvas
		var canvas = document.getElementById('game_canvas');
		var context = canvas.getContext('2d');
	
		// Set frame rate to 30 frames per second
		var run_game = setInterval(run,  1000/30);
	
		// Control user paddle:
		// clientY read-only property returns the vertical coordinate within the
		// application's client area at which the event occurred (as opposed to
		// the coordinates within the page)
		canvas.addEventListener('mousemove', function (e) {
				paddle1_y = e.clientY - paddle_height/2;
		});

		function reset_ball() {
				// Reset the ball's placement and direction after scoring
				ball_x = canvas.width / 2;
				ball_y = canvas.height/ 2;
				x_velocity = -x_velocity;
				y_velocity = 10;
		}
	
		function move_ball(){
				// Get the ball moving
				ball_x += x_velocity;
				ball_y += y_velocity;
		}

		function computer_paddle() {
				// Move the player 2 AI paddle up or down
				// based on the 'y' position of the ball
				if (paddle2_y + paddle_height/2 < ball_y){
						paddle2_y += computer_speed;
				} else {
						paddle2_y -= computer_speed;
				}
		}
	
		function bounce_off(){
			// Bounce the ball off the top of the screen
				if (ball_y < 0 && y_velocity < 0){
						y_velocity = -y_velocity;
				}

				// Bounce the ball off the bottom of the screen
				if (ball_y > canvas.height && y_velocity > 0){
						y_velocity = -y_velocity;
				}

				// Bounce the ball off the left side (where paddle)
				// Otherwise award a point to the other player
				// and reset the ball
				if (ball_x < 0){
						if (ball_y > paddle1_y && ball_y < paddle1_y + paddle_height) {
								x_velocity =- x_velocity;
								delta_y = ball_y - (paddle1_y + paddle_height/2);
								y_velocity = delta_y * 0.3;
						} else {
								player2_score++;
								reset_ball();
						}
				}

				// Bounce the ball off the right side (where paddle)
				// Otherwise award a point to the other player
				// and reset the ball
				if (ball_x > canvas.width){
						if (ball_y > paddle2_y && ball_y < paddle2_y + paddle_height) {
								x_velocity =- x_velocity;
								delta_y = ball_y - (paddle2_y + paddle_height/2);
								y_velocity = delta_y * 0.3;
						} else {
								player1_score++;
								reset_ball();
						}
				}
		}
	
		function setup_canvas() {
				//fill in the canvas with objects
				context.fillStyle = 'blue';
				context.fillRect(0, 0, canvas.width, canvas.height);

				// Add the paddles' color
				context.fillStyle = 'white';

				// Add paddle 1
				context.fillRect(0, paddle1_y, paddle_thickness, paddle_height);

				// Add paddle 2
				context.fillRect(canvas.width-paddle_thickness, paddle2_y, paddle_thickness, paddle_height);

				// Draw the ball
				context.fillRect(ball_x-ball_dimension/2, ball_y-ball_dimension/2, ball_dimension, ball_dimension);

				// Add Score board boxes
				context.fillRect(90, canvas.height - 95, 40, 40);
				context.fillRect(canvas.width - 110, 65, 40, 40);
			
				// Add the score text
				context.font = "18px serif";
				context.fillText("Your Score", 70, canvas.height - 40);
				context.fillText("AI Score", canvas.width - 120, 60);
				context.fillStyle = 'black';
				context.font = "48px serif";
				context.fillText(player1_score, 100, canvas.height - 60);
				context.fillText(player2_score, canvas.width - 100, 100);
		}
	
		function did_player_win(){
			if(player1_score === winning_score || player2_score === winning_score){
				// set variable to reset game
				reset_game = true;
				// stop the game from running
				clearTimeout(run_game);
				context.fillStyle = 'white';
				context.font = "48px serif";
				context.fillText("End of Game", canvas.width/2 - canvas.width/6, canvas.height/2);
				if (player1_score === winning_score){
					context.font = "24px serif";
					context.fillText("You won!", canvas.width/2 - canvas.width/14, canvas.height/2 + 25);
				} 
				if (player2_score === winning_score){
					context.font = "24px serif";
					context.fillText("The AI won!", canvas.width/2 - canvas.width/14, canvas.height/2 + 25);
				}
			}
		}
	

		function run(){
				move_ball();
				bounce_off();
				computer_paddle();
				setup_canvas();
				did_player_win();
				// Make sure the game stops
				// console.log('running');
		}
}
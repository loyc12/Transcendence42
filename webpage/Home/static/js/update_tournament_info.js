
let update_tournament_brackets = function(bracket_info) {
    
    if (isTournament) {
        player1Login = bracket_info[0].login;
        player2Login = bracket_info[1].login;
        player3Login = bracket_info[2].login;
        player4Login = bracket_info[3].login;

        document.getElementById('nameP1').innerHTML = 'player1Login';
        document.getElementById('nameP2').innerHTML = 'player2Login';
        document.getElementById('nameP3').innerHTML = 'player3Login';
        document.getElementById('nameP4').innerHTML = 'player4Login';

        document.getElementById('scoreP1').innerHTML = '---';
        document.getElementById('scoreP2').innerHTML = '---';
        document.getElementById('scoreP3').innerHTML = '---';
        document.getElementById('scoreP4').innerHTML = '---';

        if (isGhostLobby){
            player1Winner = bracket_info[0].winner;
            player2Winner = bracket_info[1].winner;
            document.getElementById('nameWinner1').innerHTML = 'player1Winner';
            document.getElementById('scoreWinner1').innerHTML = '---';
            document.getElementById('nameWinner2').innerHTML = 'player2Winner';
            document.getElementById('scoreWinner2').innerHTML = '---';

            player1Score1 = bracket_info[0].score;
            player2Score1 = bracket_info[1].score;
            player3Score1 = bracket_info[2].score;
            player4Score1 = bracket_info[3].score;
    
            document.getElementById('scoreP1').innerHTML = 'player1Score1';
            document.getElementById('scoreP2').innerHTML = 'player2Score1';
            document.getElementById('scoreP3').innerHTML = 'player3Score1';
            document.getElementById('scoreP4').innerHTML = 'player4Score1';
        }
    }
}


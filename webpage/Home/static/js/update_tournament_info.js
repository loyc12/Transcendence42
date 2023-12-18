
let mock_groupA = {
    p1: {
        login: 'Player1',
        score: '1',
    },
    p2: {
        login: 'Player2',
        score: '1',
    }
}

let mock_groupB = {
    p3: {
        login: 'Player3',
        score: '1',
    },
    p4: {
        login: 'Player4',
        score: '1',
    }
}

let update_tournament_brackets = function() {
    
    //  GROUP A
    document.getElementById('nameP1').innerHTML = mock_groupA.p1.login;
    document.getElementById('scoreP1').innerHTML = mock_groupA.p1.score;

    document.getElementById('nameP2').innerHTML = mock_groupA.p2.login;
    document.getElementById('scoreP2').innerHTML = mock_groupA.p2.score;

    //  GROUP B
    document.getElementById('nameP3').innerHTML = mock_groupB.p3.login;
    document.getElementById('scoreP3').innerHTML =  mock_groupB.p3.score;

    document.getElementById('nameP4').innerHTML = mock_groupB.p4.login;
    document.getElementById('scoreP4').innerHTML = mock_groupB.p4.score;

    //  GROUP C
    document.getElementById('nameWinner1').innerHTML = mock_groupA.p1.login;
    document.getElementById('scoreWinner1').innerHTML = 1;
    document.getElementById('nameWinner2').innerHTML = mock_groupB.p3.login;
    document.getElementById('scoreWinner2').innerHTML = 2;

    // WINNNER

    // if (data.init.tournament.groupC)
    // {
    //     document.getElementById('scoreP1') = data.init.tournament.groupA.p1.score;
    //     document.getElementById('scoreP2') = data.init.tournament.groupA.p2.score;
    //     document.getElementById('scoreP3') = data.init.tournament.groupB.p3.score;
    //     document.getElementById('scoreP4') = data.init.tournament.groupB.p4.score;
        
    //     document.getElementById('nameWinner1') = data.init.tournament.groupC.winner1.login;
    //     document.getElementById('nameWinner2') = data.init.tournament.groupC.winner2.login;
    // }

}



let mock_groupA = {
    p1: {
        login: 'Player1',
        score: '---',
    },
    p2: {
        login: 'Player2',
        score: '---',
    }
}

let mock_groupB = {
    p3: {
        login: 'Player3',
        score: '---',
    },
    p4: {
        login: 'Player4',
        score: '---',
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
    document.getElementById('scoreWinner1').innerHTML = '---';
    document.getElementById('nameWinner2').innerHTML = mock_groupB.p3.login;
    document.getElementById('scoreWinner2').innerHTML = '---';

    // WINNNER
}


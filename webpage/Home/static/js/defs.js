// keyboard keys
let UP =     'up';
let DOWN =   'dn';
let LEFT =   'lf';
let RIGHT =  'rt';
let SPACE =  ' ';

// keypad keys
let KW = 'w';
let KS = 's';
let KA = 'a';
let KD = 'd';
let NZERO = '0';

let START = 'start_game';
let CLOSE = 'end_game';
let KEYPRESS = 'key_press';
let ESCAPE = null;
let RETURN = null;

// Global vars declarations

let userDisconnectedSocket = false;

let gameData;/// struct returned from request_join_game()

let currentWidth;// = canvas.width;
let currentHeight;// = canvas.height;
let currentGameType;

let currentGameInfo;

let isTournament = false;
let isGhostLobby = false;

let tourWebSockID = null;
let tourWebSock = null;
let tourStage1GameData = null;
let tourStage2GameData = null;
let tourStage = null;
let isTournamentStage1 = false;
let tournamentStage1Started = false;
let isTournamentStage2 = false;
let tournamentStage2Started = false;

const playerColors = ['#ffffff', '#ff10f0', '#23e301', '#04d9ff', '#ff6700'];// index 0 is default
const playerShadowColors = ['#ffffff', '#ff10f0', '#23e301', '#04d9ff', '#ff6700'];// To be determined. index 0 is default color (AI)

// both bottom
const initPingParam = {
    'gameType': 'Ping',
    'sizeInfo': {
        'width': 2048, 'height': 1024,
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625,
        'sRacket': 160, 'sBall': 20
    },
    'racketCount': 2,
    'teamCount': 2,
    'orientations': ['x', 'x'],
    'update': {
        'racketPos': [682, 1004, 1365, 1004 ],
        "lastPonger": 0,
        'ballPos': [1024, 682],
        'scores' : [0, 0],
    }
};

// in front of each other
const initPongParam = {
     'gameType': 'Pong',
     'sizeInfo': {
        'width': 2048, 'height': 1024,
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625,
        'sRacket': 160, 'sBall': 20
    },
    'racketCount': 2,
    'teamCount': 2,
    'orientations': ['y', 'y'],
    'update': {
        'racketPos': [20, 512, 2028, 512],
        "lastPonger": 0,
        'ballPos': [1014, 512],
        'scores' : [0, 0],
    }
};

// 4 players
const initPingestParam = {
    'gameType': 'Pingest',
    'sizeInfo': {
        'width': 2048, 'height': 1024,
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625,
        'sRacket': 160, 'sBall': 20},
    'racketCount': 4,
    'teamCount': 4,
    'orientations': ['x', 'x', 'x', 'x'],
    'update': {
        'racketPos': [438, 20, 1097, 20, 438, 904, 1097, 904],
        "lastPonger": 0,
        'ballPos': [512, 512],
        'scores' : [0, 0, 0, 0],
    }
}

const allInitGameStates = new Map();
allInitGameStates.set('Local_1p', initPongParam);
allInitGameStates.set('Local_2p', initPongParam);
allInitGameStates.set('Tournament', initPongParam);
allInitGameStates.set('Multiplayer', initPingParam);
allInitGameStates.set('Online_4p', initPingestParam);

currentGameInfo = initPongParam;
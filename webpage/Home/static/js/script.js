let currrentState = 'init';

window.onpopstate = function (event) {
    if (event.state) {
        handleStateChange(event.state);
    }
};

function navigateForward(newState) {
    history.forward();
};

function handleStateChange(newState) {
    console.log('Navigated to: ', newState);
    if (newState === 'lobby' || newState === 'game' || newState === 'aftergame'|| newState === 'tournament') {
        select_hero_content('init');
    }
    else if (newState === 'info')
        select_hero_content('info');
    else if (newState === 'gameMode')
        select_hero_content('gameMode');
    else if (newState === 'gameTypeLocal')
        select_hero_content('gameTypeLocal');
    else if (newState === 'gameTypeOnline')
        select_hero_content('gameOnline');
    else
        select_hero_content('init');
};


let UP =     'up';
let DOWN =   'dn';
let LEFT =   'lf';
let RIGHT =  'rt';
let SPACE =  ' ';

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

let gameData;

let currentWidth;
let currentHeight;
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

const playerColors = ['#ffffff', '#ff10f0', '#23e301', '#04d9ff', '#ff6700'];
const playerShadowColors = ['#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff'];

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
};

const allInitGameStates = new Map();
allInitGameStates.set('Local_1p', initPongParam);
allInitGameStates.set('Local_2p', initPongParam);
allInitGameStates.set('Tournament', initPongParam);
allInitGameStates.set('Multiplayer', initPingParam);
allInitGameStates.set('Online_4p', initPingestParam);

currentGameInfo = initPongParam;


let userWebSockID = null;
let userWebSock = null;

let _on_user_event = function(event) {
    const data = JSON.parse(event.data);
};

let _on_close_disconnect = function (event) {
    console.error('Server disconnected user websocket');
};

let _build_user_ws_path = function(sockID) {
    return 'wss://' + window.location.host + '/users/ws/' + sockID + '/';
};

let _connect_to_user_socket = function (userWebSockPath) {
    let sock;
    try {
        sock = new WebSocket(userWebSockPath);
    } catch (err) {
        alert('Failed To connect to server USER websocket.')
    }
    return sock;
};

let _on_server_side_user_disconnect = function(e) {
    user_id = null;
};

let _prepare_user_websocket = function (ws) {
    userWebSock = ws;
    ws.onmessage = _on_user_event;
    ws.onclose = _on_close_disconnect;
};

if (user_id != null) {

    userWebSockID = ('USOCK' + user_id);
    let sockPath = _build_user_ws_path(userWebSockID);
    userWebSock = _connect_to_user_socket(sockPath);
    _prepare_user_websocket(userWebSock);
};


let wipe_tournament_data = function () {
    tourWebSock = null;
    tourStage1GameData = null;
    tourStage2GameData = null;
    tourStage = null;
    isTournamentStage1 = false;
    tournamentStage1Started = false;
    isTournamentStage2 = false;
    tournamentStage2Started = false
};

let _on_tour_event = function(event) {
    const data = JSON.parse(event.data);

    if (data.ev === 'game_connect') {
        reset_default_lobby();
        gameType = data.form.gameMode;
        parseInitData(get_default_init_state(gameType));
        disconnect_socket()

        let stageNB = data.stage;
        if (stageNB == '1') {
            isTournament = true;
            tourStage2GameData = null;
            tourStage = 'lobbyStage1';
            tourStage1GameData = data;
            isTournamentStage1 = true;
        }
        else if (stageNB == '2') {
            isTournament = true;
            tourStage1GameData = null;
            tourStage = 'lobbyStage2';
            tourStage2GameData = data;
            isTournamentStage2 = true;
        }
    }
};

function _build_tour_ws_path(sockID) {
    return 'wss://' + window.location.host + '/tournament/ws/' + sockID + '/';
};

let _connect_to_tour_socket = function (tourWebSockPath) {
    let sock;
    try {
        sock = new WebSocket(tourWebSockPath);
    } catch (err) {
        alert('Failed To connect to server TOURNAMENT websocket.')
    }
    return sock;
};

let _on_server_side_tour_disconnect = function(e) {
    disconnect_socket();
    wipe_tournament_data();
};

let _prepare_tour_websocket = function (ws) {
    ws.onmessage = _on_tour_event;
    ws.onclose = _on_server_side_tour_disconnect;
};

let disconnect_tour_socket = function() {
    if (tourWebSock)
        tourWebSock.close()
    tourWebSockID = null;
    tourWebSock = null;
};


let current_content = null;

let content_flush = ['NavBarInit', 'NavBarInfo', 'NavBarGame', 'NavBarLogin',
                        'contentHome', 'contentInfo', 'contentGame', 'contentLogin',
                        'gameTypeLocal', 'gameTypeOnline', 'lobby', 'game', 'aftergame', 'tournament']

let all_hero_content2 = {
    'init': {
        'navBar': 'NavBarInit',
        'heroDiv': 'contentHome'
    },
    'info': {
        'navBar': 'NavBarInfo',
        'heroDiv': 'contentInfo'
    },
    'game': {
        'navBar': 'NavBarGame',
        'heroDiv': 'contentGame'
    },
    'login': {
        'navBar': 'NavBarLogin',
        'heroDiv': 'contentLogin'
    },
};

let hide_all_hero_content = function () {

    for (c of content_flush) {
        elem = document.getElementById(c);
        if (elem)
            elem.style.display = 'none';
    }
};

let select_hero_content = function (key) {
    let contentElems = all_hero_content2[key];
    if (!contentElems)
        return;
    let navContentElem = document.getElementById(contentElems['navBar']);
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    if (navContentElem)
        navContentElem.style.display = 'block';
    if (heroContentElem)
    {
        if (contentElems['heroDiv'] === 'contentGame') {
            loadModule('gameMode')
            disconnect_socket()
            disconnect_tour_socket();
        }
        if (current_content == key)
            return ;
        else
        {
            history.pushState(key, '', null);
            hide_all_hero_content();
        }
        if (navContentElem)
            navContentElem.style.display = 'block';
        if (contentElems['heroDiv'] === 'contentInfo') {
            fetch_user_profile()
        }
        heroContentElem.style.display = 'block';
        current_content = key;
        try {
            disconnect_socket()
            disconnect_tour_socket();
        } catch {}
    }
}

let buttonModule0 = document.getElementById('buttonModuleHome');
let buttonModule1 = document.getElementById('buttonModuleInfo');
let buttonModule2 = document.getElementById('buttonModuleGame');
let buttonModule3 = document.getElementById('buttonModuleLogin');

if (buttonModule0)
    buttonModule0.addEventListener('click', function () {select_hero_content('init');})
if (buttonModule1)
    buttonModule1.addEventListener('click', function () { select_hero_content('info');})
if (buttonModule2)
    buttonModule2.addEventListener('click', function () {select_hero_content('game');})
if (buttonModule3)
    buttonModule3.addEventListener('click', function () { select_hero_content('login');})
select_hero_content('init')


let _build_join_request_payload = function (gameMode, gameType, withAI=false, eventID=0) {
    return {
        'gameMode': gameMode,
        'gameType': gameType,
        'withAI': withAI,
        'eventID': eventID
    }
  }

  let _http_join_request = async function (payload) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    return fetch('https://' + window.location.host + '/game/join/', {
        method: "POST",
        body: JSON.stringify(payload),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
    .then (function(response) {
      return response.json()
    })
    .then (function(data) {
      if (data.status === 'failure')
        alert('Join game request failed because : \n\t - ' + data.reason)
      if (data.sockID) {
        return data;
      }
    })
  }

  let request_join_game = async function (gameType) {
    currentGameType = gameType
    if (gameType === 'Local_1p') {
      payload = _build_join_request_payload('Local_1p', 'Pong', true);
    } else if (gameType === 'Local_2p') {
      payload = _build_join_request_payload('Local_2p', 'Pong', false);
    } else if (gameType === 'Tournament') {
      payload = _build_join_request_payload('Tournament', 'Pong', false);
    } else if (gameType === 'Multiplayer') {
      payload = _build_join_request_payload('Multiplayer', 'Ping', false);
    } else if (gameType === 'Online_4p') {
      payload = _build_join_request_payload('Online_4p', 'Pingest', false);
    } else {
      throw TypeError('Trying to request join game with unimplemented gameType: ' + gameType)
    }
    gameData = await _http_join_request(payload)
    return gameData;
};


// Variable to store selected options
let selectedOptions = {};

let full_game_page_states_list = ['gameMode', 'gameTypeLocal', 'gameTypeOnline', 'lobby', 'game', 'aftergame']

function loadModule(moduleName) {
    for (c of full_game_page_states_list) {
        document.getElementById(c).style.display = 'none'
    }

    if (moduleName === 'gameMode') {
        document.getElementById('gameMode').style.display = 'block';
    }
    else if (moduleName === 'local'){
        document.getElementById('gameTypeLocal').style.display = 'block';
    }
    else if (moduleName === 'online') {
        document.getElementById('gameTypeOnline').style.display = 'block';
    }
    else if (moduleName === 'lobby') {
        document.getElementById('lobby').style.display = 'block';
        if (isTournament){
            document.getElementById('tournament').style.display = 'block';
            if (isGhostLobby){
                document.getElementById('tournament').style.display = 'block';
                document.getElementById('buttonGhostLobby').style.display = 'none';
            }
        }
        else {
            document.getElementById('tournament').style.display = 'block';
        }
    }
    else if (moduleName === 'game') {
        document.getElementById('game').style.display = 'block';
    }
    else if (moduleName === 'aftergame' ) {
        if (isTournament)
            isGhostLobby = true;
        document.getElementById('aftergame').style.display = 'block';
    }
    else {
        request_join_game(moduleName)
    }
};

function loadSubModule(subModuleName) {
    selectedOptions.subModule = subModuleName;
};

let get_text_from_readable_stream = async function(stream) {
    const reader = stream.getReader();
    const { value, done } = await reader.read();
    return
  }

  let fetch_user_profile = function () {

      fetch('https://' + window.location.host + '/users/profile/get')
      .then (data => {
        elem = document.getElementById('profile');

        data.text().then(text => {
            if (elem)
                elem.innerHTML = text;
          })
      })
      .catch(function (err) {
        console.log(err);
      })
};


const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const initialWidth = canvas.width;
const initialHeight = canvas.height;

currentWidth = canvas.width;
currentHeight = canvas.height;

const initParam = {
     'gameType': 'Pong',
     'sizeInfo': {'width': 2048, 'height': 1024,
        'wRatio': 0.00048828125, 'hRatio': 0.0009765625,
        'sRacket': 160, 'sBall': 20},
    'racketCount': 2,
    'racketInitPos': [20, 512, 'x', 2028, 512, 'x'],
    'ballInitPos': [512, 512],
    'teamCount': 2
};

function printCurrentParam (currentGameInfo) {
}

let setCanvasSize = function () {
    const parent = canvas.parentElement

    canvas.width = Math.min(initialWidth, parent.clientWidth);
    canvas.height = Math.min(initialHeight, parent.clientHeight);

    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}


const prevent_keyset = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'];

let _player_event_handler = function (event) {

    if (event.repeat) {
        return;
    }
    if (prevent_keyset.indexOf(event.code) > -1) {
        event.preventDefault();
    }
    if ( event.key === 'w' || event.key === 'W') {
        _send_player_keyevent(KW);
    }
    else if ( event.key === 's' || event.key === 'S') {
        _send_player_keyevent(KS);
    }
    else if ( event.key === 'a' || event.key === 'A') {
        _send_player_keyevent(KA);
    }
    else if ( event.key === 'd' || event.key === 'D') {
        _send_player_keyevent(KD);
    }
    else if (event.key === ' ') {
        _send_player_keyevent(SPACE);
    }
    else if (event.key === "ArrowUp") {
        _send_player_keyevent(UP);
    }
    else if (event.key === "ArrowDown") {
        _send_player_keyevent(DOWN);
    }
    else if (event.key === "ArrowLeft") {
        _send_player_keyevent(LEFT)
    }
    else if (event.key === "ArrowRight") {
        _send_player_keyevent(RIGHT);
    }
    else if (event.key === '0') {
        _send_player_keyevent(NZERO);
    }
};

let activatePlayerControler = function () {
    document.addEventListener("keydown", _player_event_handler);
};

let deactivatePlayerControler = function () {
    document.removeEventListener("keydown", _player_event_handler);
};

function parseInitData (init_data) {
    if (! 'update' in init_data)
        alert("ERROR: initData received is missing the 'update' struct.")
    const { width, height } = init_data.sizeInfo;
    currentGameInfo = init_data;
    canvas.width = width;
    canvas.height = height;

    currentGameInfo.racketSize = init_data.sizeInfo.sRacket;
    currentGameInfo.ballSize = init_data.sizeInfo.sBall;

    currentGameInfo.offsets = [];
    currentGameInfo.widths = [];
    currentGameInfo.heights = [];
    for (ori of init_data.orientations) {
        if (ori === 'x') {
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sRacket * 0.5));
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sBall * 0.5));
            currentGameInfo.widths.push()
        } else if (ori === 'y') {
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sBall * 0.5));
            currentGameInfo.offsets.push(-(init_data.sizeInfo.sRacket * 0.5));
        }
    }
};

let parseUpdateData = function (update) {

    currentGameInfo.update = update;
    updateCanvas(currentGameInfo);
};

let parsePlayersInfo = function(info) {
};

let setCurrentState = function (initData) {
    currentGameInfo = initData;
    console.log('initData.game : ' + initData.gameType );
};

const players = [
    { name: 'AI', rank: 0},
    { name: 'Player 1', rank: 1 },
    { name: 'Player 2', rank: 2 },
    { name: 'Player 3', rank: 3 },
    { name: 'Player 4', rank: 4 },
];

let getPlayerColor = function(rank) {
    const index = (rank + 1) % playerColors.length;
    return playerColors[index];
};

let getPlayerShadowColor = function(rank) {
    const index = (rank + 1) % playerColors.length;
    return playerShadowColors[index];
};

let clearCanvas = function (ctx, w, h) {
    ctx.clearRect(0, 0, w, h);
};

let renderCanvas = function (ctx, gameInfo) {

    let scorePlayer1 = [(canvas.width / 2 - 140 ) , 250];
    let scorePlayer2 = [(canvas.width / 2 + 100 ) , 250];
    let scorePlayer3 = [(canvas.width / 2 - 140 ) , (canvas.height - 250)];
    let scorePlayer4 = [(canvas.width / 2 + 100 ) , (canvas.height - 250)];

    renderBall(ctx, gameInfo, gameInfo.update);
    renderRackets(ctx, gameInfo, gameInfo.update);

    ctx.font = "64px Arial";
    ctx.fillStyle = "gray";
    ctx.fillRect(canvas.width / 2, 0, 1, canvas.height);
    ctx.fillStyle = "white";

    ctx.fillText(gameInfo.update.scores[0], scorePlayer1[0], scorePlayer1[1]);
    ctx.fillText(gameInfo.update.scores[1], scorePlayer2[0], scorePlayer2[1]);
    if (gameInfo.gameType === 'Pingest') {
        ctx.fillText(gameInfo.update.scores[2], scorePlayer3[0], scorePlayer3[1]);
        ctx.fillText(gameInfo.update.scores[3], scorePlayer4[0], scorePlayer4[1]);
    }
};

let renderBall = function (ctx, gameInfo, update) {
    const x = update.ballPos[0];
    const y = update.ballPos[1];
    let ballColorLast = getPlayerColor(update.lastPonger - 1);
    const shadow = getPlayerShadowColor(update.lastPonger - 1);
    ctx.beginPath();
    ctx.shadowBlur = 40;
    ctx.fillStyle = ballColorLast;
    ctx.shadowColor = shadow;
    ctx.arc(x, y, gameInfo.ballSize * 0.5, 0, 2 * Math.PI);
    ctx.fill();
};

let renderRackets = function(ctx, gameInfo, update) {
    let orientations = gameInfo.orientations;
    let racketCount = gameInfo.racketCount;
    let x, y, w, h;
    let color, shadow;

    for (let i = 0; i < racketCount; i++) {
        x = update.racketPos[2*i] + currentGameInfo.offsets[2*i];
        y = update.racketPos[2*i + 1] + currentGameInfo.offsets[2*i + 1];
        color = getPlayerColor(i);
        if (gameInfo.gameType === 'Pong' && i > 2) {
            color = '#ffffff';   }
        shadow = getPlayerShadowColor(i);
        console.log('orientation = ' + orientations[i]);
        if (orientations[i] === 'x') {
            w = gameInfo.racketSize;
            h = gameInfo.ballSize;
        }
        else if (orientations[i] === 'y') {
            w = gameInfo.ballSize;
            h = gameInfo.racketSize;
        }

        ctx.fillStyle = color;
        ctx.shadowBlur = 40;
        ctx.shadowColor = shadow;
        ctx.fillRect(x, y, w, h);
    }
};

let updateCanvas = function (gameInfo) {
    clearCanvas(ctx, canvas.width, canvas.height);
    renderCanvas(ctx, gameInfo);
};


var gameSockID = null;
var gameEventID = null;
var gameWebSockPath = null;
var gameWebSock = null;

let _send_player_keyevent = function(key) {
    payload = JSON.stringify({
        'ev': KEYPRESS,
        'key': key
    })
    gameWebSock.send(payload)
}

let _get_websocket_path = function(sockID) {
    return 'wss://' + window.location.host + '/game/ws/' + sockID + '/';
}

let _on_game_event = function(event) {
    const data = JSON.parse(event.data);

    if (data.ev === 'up') {
        parseUpdateData(data.state)
    }
    else if (data.ev === "init") {
        parseInitData(data.init)
    }
    else if (data.ev === 'connection') {
        update_player_info(data.player_list)
    }
    else if (data.ev === "start") {
        loadGame()
    }
    else if (data.ev === "end") {
        loadEndGame(data.end_state);
    }
}

let _on_server_side_disconnect = function(e) {
    gameWebSock = null;
    gameSockID = null;
    gameEventID = null;
    gameWebSockPath = null;
    if (isTournamentStage1 && !tournamentStage1Started) {
        gameSockID = tourStage1GameData.sockID;
        gameEventID = tourStage1GameData.form.eventID;
        gameWebSockPath = _get_websocket_path(gameSockID);
        gameWebSock = _connect_to_game_socket(gameWebSockPath);
        _prepare_websocket(gameWebSock);
        tournamentStage1Started = true;
    }
    else if (isTournamentStage2 && !tournamentStage2Started) {
        gameSockID = tourStage2GameData.sockID;
        gameEventID = tourStage2GameData.form.eventID;
        gameWebSockPath = _get_websocket_path(gameSockID);
        gameWebSock = _connect_to_game_socket(gameWebSockPath);
        _prepare_websocket(gameWebSock);
        tournamentStage2Started = true;
    }
};

let _connect_to_game_socket = function (gameWebSockPath) {
    let sock;

    try {
        sock = new WebSocket(gameWebSockPath);
    } catch (err) {
        alert('Failed To connect to server websocket.')
    }
    return sock;
}


let _prepare_websocket = function (ws) {
    gameWebSock = ws;
    ws.onmessage = _on_game_event;
    ws.onclose = _on_server_side_disconnect;
}

let disconnect_socket = function() {
    if (gameWebSock != null) {
        gameWebSock.close()

        gameSockID = null;
        gameWebSockPath = null;
    }
    deactivatePlayerControler()
}

let get_default_init_state = function(gameType) {
    if (! gameType in allInitGameStates)
        alert(`gameType ${gameType} not found in allInitGameStates`);
    return allInitGameStates.get(gameType);
}

let loadMegaModule = function (gameType) {
    if (gameWebSock != null) {
        alert("You can't connect to a game while already connected to another.")
        throw new EvalError("You can't connect to a game while already connected to another.");
    }
    reset_default_lobby();
    parseInitData(get_default_init_state(gameType));
    updateCanvas(currentGameInfo);
    request_join_game(gameType)
        .then(function (gameData) {
            if (!gameData.sockID)
                throw new EvalError('Request Join Game FAILED !');
            gameSockID = gameData.sockID;
            gameWebSockPath = _get_websocket_path(gameData.sockID);
            if (gameData.gameMode === 'Tournament')
            {
                tourWebSockID = gameData.tourSockID;
                tourWebSockPath = _build_tour_ws_path(tourWebSockID);
                console.log('Tournament socket path : ' + tourWebSockPath);
                tourWebSock = _connect_to_tour_socket(tourWebSockPath)
                _prepare_tour_websocket(tourWebSock);
                isTournament = true;
            }
            else if (!isTournament){
                wipe_tournament_data();
            }
            loadModule('lobby');
            return _connect_to_game_socket(gameWebSockPath);
        })
        .then(function (gameWebSock) {
            _prepare_websocket(gameWebSock);
        })
        .catch(e => {
            console.error('Exeption while requesting to join game : ' + e)
        })
};

let loadGame = function() {
    loadModule('game');
    activatePlayerControler();
};


const default_lobby_template = document.getElementById('lobby').innerHTML;

let reset_default_lobby = function () {
  document.getElementById('lobby').innerHTML = default_lobby_template;
}

let hide_excess_player_profiles = function (nb_rackets) {
  for (let i=0; i < 4; i++) {
    profElemID = `lobbyProfile${i + 1}`;
    profElem = document.getElementById(profElemID);
    if (i < nb_rackets)
      profElem.style.display = 'flex';
    else
      profElem.style.display = 'none';
  }
}

let update_local_1p_info = function (player_info) {
  document.getElementById("imgPlayer1").src = player_info.img;
  document.getElementById("namePlayer1").innerHTML = player_info.login;
  document.getElementById("imgPlayer2").style.border = "3px outset #34eb34";
  document.getElementById("namePlayer2").innerHTML = "Celine Incognito";
}

let update_local_2p_info = function (player_info) {
  document.getElementById("imgPlayer1").src = player_info.img;
  document.getElementById("namePlayer1").innerHTML = player_info.login;
  document.getElementById("imgPlayer2").style.border = "3px outset #34eb34";
  document.getElementById("namePlayer2").innerHTML = "Guest";
}


let update_player_info = function (player_info_list) {
  document.getElementById("startEngine").disabled = false;
  reset_default_lobby()
  if (isTournament)
    hide_excess_player_profiles(4);
  else
    hide_excess_player_profiles(currentGameInfo.racketCount);

  if (currentGameType === 'Local_1p')
    update_local_1p_info(player_info_list[0]);
  else if (currentGameType === 'Local_2p')
    update_local_2p_info(player_info_list[0]);

  else {
    let i = 0;
    for (ply of player_info_list) {
      imgElemID = `imgPlayer${++i}`;
      nameElemID = `namePlayer${i}`;
      login = ply.login;
      img = ply.img;
      ready = ply.ready;

      document.getElementById(imgElemID).src = img;
      document.getElementById(nameElemID).innerHTML = ` ${login}`;
      if (ready)
      {
        document.getElementById(imgElemID).style.border = "3px outset #34eb34";
      }
    }
  }
};

let on_click_update_players = function () {
  update_player_info(mock_player_list);
};

let signal_player_ready = function() {
  document.getElementById("startEngine").disabled = true;
  document.getElementById("startEngine").innerHTML = "READY!";
  document.getElementById("custom-spinner").style.display = "block";
  let payload = {
    'ev': 'ready'
  }
  gameWebSock.send(JSON.stringify(payload));
}

let reset_endgame_messages = function () {
  document.getElementById("winner").style.display = "none";
  document.getElementById("loser").style.display = "none";
  document.getElementById("crash").style.display = "none";
  document.getElementById("finish").style.display = "none";
}

let loadEndGame = function (data) {
  reset_endgame_messages();
  loadModule('aftergame');
  console.log('data : ' +  data)
  console.log('winnerID : ' +  data.winningTeam)
  console.log('data.winningTeam : ' + data.winningTeam)
  console.log('data.playerInfo : ' + data.playerInfo)

  let winnerID = data.winningTeam;
  console.log('data.winningTeam : ' + data.winningTeam) //	NOTE (LL) : if winningTeam == 0, no winner
  let winner = data.playerInfo[winnerID];
  console.log('data.winner : ' + data.winner)
  let user_is_winner = (parseInt(winner.playerID) == user_id);
  console.log('user_is_winner : ' + user_is_winner)
  //   let user_is_winner = data.playerInfo[winnerID];


  document.getElementById("buttonGhostLobby").style.display = "none";

  if (winnerID == undefined){
    document.getElementById("crash").style.display = "block";
  }
  else if (currentGameType === 'Local_1p' || currentGameType === 'Local_2p' ) {
    document.getElementById("finish").style.display = "block";
  }
  else if (user_is_winner ) {
    document.getElementById("winner").style.display = "block";
    if (isTournament){
      document.getElementById("buttonGhostLobby").style.display = "block";
      if (isGhostLobby)
        document.getElementById("buttonGhostLobby").style.display = "none";
    }
  }
  else if (data.endState === 'crash'){
    document.getElementById("loser").style.display = "block";
  }
  else if (data.endState === 'wall_of_shame'){
    document.getElementById("wallofshame").style.display = "block";
  }
}

let signal_final_game = function() {
  if (tourWebSock == null) {
    disconnect_socket();
    disconnect_tour_socket();
    return;
  }
  let payload = JSON.stringify({
    'ev': 'final'
  });
  loadModule('lobby');
  tourWebSock.send(payload);
};


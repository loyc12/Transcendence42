
let current_content = null;

let navigationState = [];


let content_flush = ['NavBarInit', 'NavBarInfo', 'NavBarGame', 'NavBarLogin', 'NavBarHelp',
                        'contentHome', 'contentInfo', 'contentGame', 'contentLogin', 'contentHelp',
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
    'help': {
        'navBar': 'NavBarHelp',
        'heroDiv': 'contentHelp'
    },
}

let hide_all_hero_content = function () {

    for (c of content_flush) {
        elem = document.getElementById(c);
        if (elem)
            elem.style.display = 'none';
    }
}

function pushStateAndUpdate(state, title) {
    stateID = stateID + 1;
    var pstate = {
        "state": state,
        "id": stateID
    }
    console.log(" -- history len before push : " + window.history.length);
    console.log(" -- history state before push : " + window.history.state.state);

    window.history.pushState(pstate, "", null);
    console.log(" -- history len after push : " + window.history.length);
    console.log(" -- history state after push : " + window.history.state.state);
  }

let select_hero_content = function (key, doPushState=true) {
    let contentElems = all_hero_content2[key];
    if (!contentElems)
        return;

    let navContentElem = document.getElementById(contentElems['navBar']);
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    if (navContentElem){
        navContentElem.style.display = 'block';
    }
    else
        console.log('navContentElem NOT FOUND')
    if (heroContentElem)
    {
        if (contentElems['heroDiv'] === 'contentGame') {
            loadModule('gameMode')
            disconnect_socket()
            disconnect_tour_socket()
        }
        // Herodiv = [ help ]
        if (contentElems['heroDiv'] === 'contentHelp') {
            loadModule('help')
        }
        // Herodiv = [ contentInfo ]
        if (contentElems['heroDiv'] === 'contentInfo') {
            fetch_user_profile()
        }

        if (current_content == key)
            return ;
        else
        {
            // set hash tag to dont know what here , but smthimg changed!!!
            console.log('[[]] currentContent is ', current_content, '!= key __ ', key);
            console.log('[[** after pushState history len == ' + window.history.length)
            console.log('[[** after pushState history.state == ' + window.history.state)
            console.log('[[]] navigationState len == ' + navigationState.length)

            hide_all_hero_content();
        }
        if (navContentElem)
        {
            navContentElem.style.display = 'block';
        }
        else
            console.log('navContentElem NOT FOUND')

        heroContentElem.style.display = 'block';
        current_content = key;
        if (doPushState)
            pushStateAndUpdate(current_content, current_content);
        try {
            disconnect_socket()// Closes the currently open game websocket if exists, else does nothing.
            disconnect_tour_socket()
            if (userDisconnectedSocket) {
                disconnect_user_socket();
                fetch_user_logout();
                display_unsubscribed_html();
                userDisconnectedSocket = false;
            }
        }
        catch (err) {
            console.log('ERROR : failed to disconnect sockets : ' + err);
        }
    }
    else
        console.log('heroContentElem NOT FOUND ...')
}

let buttonModule0 = document.getElementById('buttonModuleHome');
let buttonModule1 = document.getElementById('buttonModuleInfo');
let buttonModule2 = document.getElementById('buttonModuleGame');
let buttonModule3 = document.getElementById('buttonModuleLogin');
let buttonModule4 = document.getElementById('buttonModuleHelp');


if (buttonModule0)
    buttonModule0.addEventListener('click', function () {select_hero_content('init');})
if (buttonModule1)
    buttonModule1.addEventListener('click', function () { select_hero_content('info');})
if (buttonModule2)
    buttonModule2.addEventListener('click', function () {select_hero_content('game');})
if (buttonModule3)
    buttonModule3.addEventListener('click', function () { select_hero_content('login');})
if (buttonModule4)
    buttonModule4.addEventListener('click', function () { select_hero_content('help');})
// select_hero_content('init')


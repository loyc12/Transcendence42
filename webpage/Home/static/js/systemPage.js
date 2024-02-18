
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
    console.log('((INFO)) pushStateAndUpdate => ', state);
    stateID = stateID + 1;
    var pstate = {
        "state": state,
        "id": stateID
    }
    console.log(" -- history len before push : " + window.history.length);
    console.log(" -- history state before push : " + window.history.state.state);

    window.history.pushState(pstate, "", null);
    // window.history.replaceState(pstate, "", null);
    //window.history.go(1);
    console.log(" -- history len after push : " + window.history.length);
    console.log(" -- history state after push : " + window.history.state.state);
    //navigationState.push(pstate);
    // Add additional logic to update the content based on the state
    //console.log(navigationState);
  }

let select_hero_content = function (key, doPushState=true) {

    //// console.log('select_hero_content after hide')
    console.log('=== select_hero_content >> ', key);

    let contentElems = all_hero_content2[key];
    if (!contentElems)
        return;

    ///
    let navContentElem = document.getElementById(contentElems['navBar']);
    // console.log('>>> select_hero_content after navContentElem' + navContentElem + ' :  KEY >> ' + key );
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    // console.log('>>> select_hero_content after heroContentElem' + heroContentElem + ' :  KEY >> ' + key );
    ///
    if (navContentElem){
        // console.log('__Set navContent--block');
        navContentElem.style.display = 'block';
    }
    else
        console.log('navContentElem NOT FOUND')
    ///
    if (heroContentElem)
    {
        //// -----
        // console.log('__Set heroContent__');
        // Herodiv = [local | remote ]
        if (contentElems['heroDiv'] === 'contentGame') {
            console.log('Special case contentGame loadModule(gameMode)')
            // set hash tag to game here
            // location.hash = 'game'
            loadModule('gameMode')
            console.log('select_hero_content :: 1 :: disconnecting sockets ');
            disconnect_socket()
            disconnect_tour_socket()
        }
        // Herodiv = [ help ]
        if (contentElems['heroDiv'] === 'contentHelp') {
            console.log('Special case contentHelp loadModule(Help)')
            // set hash tag to help here
            // location.hash = 'help'
            loadModule('help')
        }
        // Herodiv = [ contentInfo ]
        if (contentElems['heroDiv'] === 'contentInfo') {
            console.log('Special case contentInfo : fetch profile template.')
            // location.hash = 'info'
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

        ///
        if (navContentElem)
        {
            // location.hash = 'init;'
            // console.log('[[[ navContentElem ]]] ??? block display ...', location.hash );
            navContentElem.style.display = 'block';
        }
        else
            console.log('navContentElem NOT FOUND')
        ///

        console.log('heroContentElem ' + contentElems['heroDiv'] + ' FOUND !')
        heroContentElem.style.display = 'block';
        current_content = key;
        // if (current_content != location.hash){
            // console.log('** location.hash : ' + location.hash)
        if (doPushState)
            pushStateAndUpdate(current_content, current_content);
        // }

        console.log('** current content page : ' + current_content)
        // console.log("--- [] [] systemPage VALUE navigationState [] []: ", navigationState);

        //// -----
        
        if (current_content === 'login')
        {
            console.log('Special case login : a suivre')
        }
        try {
            console.log('select_hero_content :: 3 :: disconnecting sockets ');
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


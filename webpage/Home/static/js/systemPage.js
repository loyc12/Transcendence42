
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
    history.pushState(state, title);
    navigationState.push(state);
    // Add additional logic to update the content based on the state
  }

let select_hero_content = function (key) {

    //// console.log('select_hero_content after hide')
    let contentElems = all_hero_content2[key];
    if (!contentElems)
        return;
    ///
    let navContentElem = document.getElementById(contentElems['navBar']);
    //// console.log('>>> select_hero_content after navContentElem' + navContentElem + ' :  KEY >> ' + key );
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    console.log('>>> select_hero_content after heroContentElem' + heroContentElem + ' :  KEY >> ' + key );
    ///
    if (navContentElem)
        navContentElem.style.display = 'block';
    else
        console.log('navContentElem NOT FOUND')
    ///
    if (heroContentElem)
    {
        //// -----
        // Herodiv = [local | remote ]
        if (contentElems['heroDiv'] === 'contentGame') {
            console.log('Special case contentGame loadModule(gameMode)')
            // set hash tag to game here
            location.hash = 'game'
            // history.pushState(localStorage, location.hash);
            pushStateAndUpdate(location.hash, location.hash);
            loadModule('gameMode')
            console.log('select_hero_content :: 1 :: disconnecting sockets ');
            disconnect_socket()
            disconnect_tour_socket()
        }
        // Herodiv = [ help ]
        if (contentElems['heroDiv'] === 'contentHelp') {
            console.log('Special case contentHelp loadModule(Help)')
            // set hash tag to help here
            location.hash = 'help'
            // history.pushState(localStorage, location.hash);
            pushStateAndUpdate(location.hash, location.hash);
            loadModule('help')
        }
        // Herodiv = [ contentInfo ]
        if (contentElems['heroDiv'] === 'contentInfo') {
            console.log('Special case contentInfo : fetch profile template.')
            location.hash = 'info'
            // history.pushState(window.localStorage, location.hash);
            pushStateAndUpdate(location.hash, location.hash);
            fetch_user_profile()
        }
        
        if (current_content == key)
            return ;
        else
        {
            // set hash tag to dont know what here , but smthimg changed!!!
            // history.pushState(window.localStorage, key);
            //// console.log('** pushState history ADD content page : : ' + key)
            console.log('** after pushState history len == ' + history.length)
            console.log("** History.state after pushState: ", history.state);
            console.log("--- [] [] systemPage VALUE navigationState [] []: ", navigationState);
            hide_all_hero_content();
        }

        ///
        if (navContentElem)
        {
            console.log('[[[navContentCall]]] init!?');
            location.hash = 'init';
            // pushStateAndUpdate(location.hash, location.hash);
            navContentElem.style.display = 'block';
        }
        else
            console.log('navContentElem NOT FOUND')
        ///

        console.log('heroContentElem ' + contentElems['heroDiv'] + ' FOUND !')
        heroContentElem.style.display = 'block';
        current_content = key;
        console.log('** current content page : ' + current_content)
        //// -----
        
        if (current_content === 'login')
        {
            console.log('Special case login : a suivre')
        }
        try {
            console.log('select_hero_content :: 3 :: disconnecting sockets ');
            disconnect_socket()// Closes the currently open websocket if exists, else does nothing.
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


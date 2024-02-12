
let current_content = null;

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

let select_hero_content = function (key) {

    console.log('select_hero_content after hide')
    let contentElems = all_hero_content2[key];
    if (!contentElems)
        return;
    let navContentElem = document.getElementById(contentElems['navBar']);
    console.log('>>> select_hero_content after navContentElem' + navContentElem + ' :  KEY >> ' + key );
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    if (navContentElem)
        navContentElem.style.display = 'block';
    else
        console.log('navContentElem NOT FOUND')

    if (heroContentElem)
    {
        // Herodiv = [local | remote ]
        if (contentElems['heroDiv'] === 'contentGame') {
            console.log('Special case contentGame loadModule(gameMode)')
            loadModule('gameMode')
            console.log('select_hero_content :: 1 :: disconnecting sockets ');
            disconnect_socket()
            disconnect_tour_socket()
        }
        if (contentElems['heroDiv'] === 'contentHelp') {
            console.log('Special case contentHelp loadModule(Help)')
            loadModule('help')
        }
        console.log('** Current content vs requested content : ' + current_content + ' vs ' + key)
        // console.log('previous content page : ' + key)

        if (current_content == key)
            return ;
        else
        {
            // Should be null because we haven't modified the history stack yet
            // console.log("--** History.state before pushState: ", history.state);
            // console.log('** before pushState history len == ' + history.length)
            
            history.pushState(key, '');
            console.log('** pushState history ADD content page : : ' + key)
            console.log('** after pushState history len == ' + history.length)
            console.log("==** History.state after pushState: ", history.state);
            hide_all_hero_content();
        }

        if (navContentElem)
            navContentElem.style.display = 'block';
        else
            console.log('navContentElem NOT FOUND')

        if (contentElems['heroDiv'] === 'contentInfo') {
            console.log('Special case contentInfo : fetch profile template.')
            fetch_user_profile()
        }
        console.log('heroContentElem ' + contentElems['heroDiv'] + ' FOUND !')
        heroContentElem.style.display = 'block';
        current_content = key;
        console.log('** current content page : ' + current_content)
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
select_hero_content('init')


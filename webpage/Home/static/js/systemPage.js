
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
}

let hide_all_hero_content = function () {
    
    for (c of content_flush) {
        elem = document.getElementById(c);
        if (elem)
            elem.style.display = 'none';
    }
}

let select_hero_content = function (key) {
    //hide_all_hero_content();
    console.log('select_hero_content after hide')
    let contentElems = all_hero_content2[key];
    if (!contentElems) 
        return;
    let navContentElem = document.getElementById(contentElems['navBar']);
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
            disconnect_socket()
        }
        console.log('Current content vs requested content : ' + current_content + ' vs ' + key)
        if (current_content == key)
            return ;
        else
            hide_all_hero_content();
        
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
        console.log('current content page : ' + current_content)
        
        try {
            disconnect_socket()// Closes the currently open websocket if exists, else does nothing.
        } catch {}
    }
    else
        console.log('heroContentElem NOT FOUND ...')
}

let buttonModule0 = document.getElementById('buttonModuleHome');
let buttonModule1 = document.getElementById('buttonModuleInfo');
let buttonModule2 = document.getElementById('buttonModuleGame');
let buttonModule3 = document.getElementById('buttonModuleLogin');

if (buttonModule0)
    buttonModule0.addEventListener('click', function () {select_hero_content('init');})
if (buttonModule1)
    buttonModule1.addEventListener('click', function () {select_hero_content('info');})
if (buttonModule2)
    buttonModule2.addEventListener('click', function () {select_hero_content('game');})
if (buttonModule3)
    buttonModule3.addEventListener('click', function () {select_hero_content('login');})
select_hero_content('init')


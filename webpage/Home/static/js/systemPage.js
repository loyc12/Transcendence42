// let all_hero_content = [
//     'content0',// <div id="content0" class="col-12 HeroDiv">
//     'content1',//<div id="content1" class="module1">
//     'content2',//<div id="content2" class="module2"></div>
//     'content3',//<div id="content3" class="module3">
// ]

let content_flush = ['NavBarInit', 'NavBarInfo', 'NavBarGame', 'NavBarLogin',
                        'contentHome', 'contentInfo', 'contentGame', 'contentLogin',
                        'gameTypeLocal', 'gameTypeOnline', 'lobby']

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
// let hide_all_hero_content = function () {
//     let contentElem;

//     for (c of all_hero_content) {
//         contentElem = document.getElementById(c);
//         if (contentElem)
//             contentElem.style.display = 'none';
//     }
// }

let select_hero_content = function (key) {
    hide_all_hero_content();
    console.log('select_hero_content after hide')
    let contentElems = all_hero_content2[key];
    //console.log('all_hero_content2 : ' + all_hero_content2)
    //console.log('key : ' + key)
    //console.log('all_hero_content2[key] : ' + all_hero_content2[key])
    //console.log('contentElems : ' + contentElems)
    if (!contentElems) 
        return;
    let navContentElem = document.getElementById(contentElems['navBar']);
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    // console.log('navContentElem: ' + navContentElem)
    // console.log('heroContentElem: ' + heroContentElem)
    if (navContentElem)
        navContentElem.style.display = 'block';
    else
        console.log('navContentElem NOT FOUND')

    if (heroContentElem)
    {
        if (contentElems['heroDiv'] === 'contentGame') {
            console.log('Special case contentGame loadModule(gameMode)')
            loadModule('gameMode')
        }
        if (contentElems['heroDiv'] === 'contentInfo') {
            console.log('Special case contentInfo : fetch profile template.')
            fetch_user_profile()
        }
        console.log('heroContentElem ' + contentElems['heroDiv'] + ' FOUND !')
        heroContentElem.style.display = 'block';
    }
    else
        console.log('heroContentElem NOT FOUND ...')
}

// let select_hero_content = function (id) {
//     hide_all_hero_content();
//     let contentElem = document.getElementById(all_hero_content[id]);
//     if (!contentElem) 
//         return;
//     contentElem.style.display = 'block';
// }

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

console.log('WOWOWOWOWOWOW')
select_hero_content('init')


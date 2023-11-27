// let all_hero_content = [
//     'content0',// <div id="content0" class="col-12 HeroDiv">
//     'content1',//<div id="content1" class="module1">
//     'content2',//<div id="content2" class="module2"></div>
//     'content3',//<div id="content3" class="module3">
// ]

let all_hero_content2 = [
    {
        'navBar': 'NavBar0',
        'heroDiv': 'content0'
    },
    {
        'navBar': 'NavBar0',
        'heroDiv': 'content1'
    },
    {
        'navBar': 'NavBar0',
        'heroDiv': 'content2'
    },
    {
        'navBar': 'NavBar0',
        'heroDiv': 'content3'
    },
]

let hide_all_hero_content = function () {
    
    let navContentElem;
    let heroContentElem;

    for (c of all_hero_content2) {
        navContentElem = document.getElementById(c['navBar']);
        heroContentElem = document.getElementById(c['heroDiv']);
        if (navContentElem)
            navContentElem.style.display = 'none';
        if (heroContentElem)
            heroContentElem.style.display = 'none';
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

let select_hero_content = function (id) {
    hide_all_hero_content();
    console.log('select_hero_content after hide')
    let contentElems = all_hero_content2[id];
    console.log('all_hero_content2 : ' + all_hero_content2)
    console.log('id : ' + id)
    console.log('all_hero_content2[id] : ' + all_hero_content2[id])
    console.log('contentElems : ' + contentElems)
    if (!contentElems) 
        return;
    let navContentElem = document.getElementById(contentElems['navBar']);
    let heroContentElem = document.getElementById(contentElems['heroDiv']);
    console.log('navContentElem: ' + navContentElem)
    console.log('heroContentElem: ' + heroContentElem)
    if (navContentElem)
        navContentElem.style.display = 'block';
    if (heroContentElem)
        heroContentElem.style.display = 'block';
}

// let select_hero_content = function (id) {
//     hide_all_hero_content();
//     let contentElem = document.getElementById(all_hero_content[id]);
//     if (!contentElem) 
//         return;
//     contentElem.style.display = 'block';
// }

let buttonModule0 = document.getElementById('buttonModule0');
let buttonModule1 = document.getElementById('buttonModule1');
let buttonModule2 = document.getElementById('buttonModule2');
let buttonModule3 = document.getElementById('buttonModule3');

buttonModule0.addEventListener('click', function () {select_hero_content(0);})
buttonModule1.addEventListener('click', function () {select_hero_content(1);})
buttonModule2.addEventListener('click', function () {select_hero_content(2);})
buttonModule3.addEventListener('click', function () {select_hero_content(3);})

console.log('WOWOWOWOWOWOW')
select_hero_content(0)


let all_hero_content = [
    'content1',
    'content2',
    'content3',
]

let hide_all_hero_content = function () {
    let contentElem;

    for (c of all_hero_content) {
        contentElem = document.getElementById(c);
        if (contentElem)
            contentElem.style.display = 'none';
    }
}

let select_hero_content = function (id) {
    hide_all_hero_content();
    let contentElem = document.getElementById(all_hero_content[id]);
    if (!contentElem) 
        return;
        contentElem.style.display = 'block';
}

let buttonLogin = document.getElementById('buttonLogin');
let buttonLogin2 = document.getElementById('buttonLogin2');
let buttonLogin3 = document.getElementById('buttonLogin3');

buttonLogin.addEventListener('click', function () {select_hero_content(0);})
buttonLogin2.addEventListener('click', function () {select_hero_content(1);})
buttonLogin3.addEventListener('click', function () {select_hero_content(2);})

/*
document.addEventListener('DOMContentLoaded', function () {
    showModule('module1'); // Show the initial module

    document.querySelector('.NavBar a[href="#module1"]').addEventListener('click', function (event) {
        event.preventDefault();
        showModule('module1');
    });

    document.querySelector('.NavBar a[href="#module2"]').addEventListener('click', function (event) {
        event.preventDefault();
        showModule('module2');
    });

});

function showModule(moduleId) {
    // Hide all modules
    var modules = document.querySelectorAll('.HeroDiv');
    modules.forEach(function (module) {
        module.classList.remove('active');
        history.replaceState({}, document.title, window.location.pathname);
    });

    // Show the selected module
    document.getElementById(moduleId).classList.add('active');
}

*/
let all_hero_content = [
    'content0',
    'content1',
    'content2',
    'content3',
    'content4',
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

let buttonModule0 = document.getElementById('buttonModule0');
let buttonModule1 = document.getElementById('buttonModule1');
let buttonModule2 = document.getElementById('buttonModule2');
let buttonModule3 = document.getElementById('buttonModule3');
let buttonModule4 = document.getElementById('buttonModule4');

buttonModule0.addEventListener('click', function () {select_hero_content(0);})
buttonModule1.addEventListener('click', function () {select_hero_content(1);})
buttonModule2.addEventListener('click', function () {select_hero_content(2);})
buttonModule3.addEventListener('click', function () {select_hero_content(3);})
buttonModule4.addEventListener('click', function () {select_hero_content(4);})

select_hero_content(0)


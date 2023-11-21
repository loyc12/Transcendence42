let all_hero_content = [
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

let buttonModule1 = document.getElementById('buttonModule1');
let buttonModule2 = document.getElementById('buttonModule2');
let buttonModule3 = document.getElementById('buttonModule3');
let buttonModule4 = document.getElementById('buttonModule4');

buttonModule1.addEventListener('click', function () {select_hero_content(0);})
buttonModule2.addEventListener('click', function () {select_hero_content(1);})
buttonModule3.addEventListener('click', function () {select_hero_content(2);})
buttonModule4.addEventListener('click', function () {select_hero_content(3);})

select_hero_content(0)

let currentState = 'home';  // Initialize the current state to 'home'
let initialChoice = null;    // Keep track of the initial choice

function showSubMenu(selectedOption) {
    // Check if the selected option is to the left of the current state
    const selectedOptionIndex = ['home','display', 'game', 'option'].indexOf(selectedOption);
    const currentStateIndex = ['home','display', 'game', 'option'].indexOf(currentState);

    if (selectedOption === 'home') {
        // Handle the 'Home' option
        if (currentState !== 'home') {
            currentState = 'home';
            initialChoice = null;
            initState();  // Call initState to update the navbar row
        }
    } else if (selectedOptionIndex < currentStateIndex) {
        // Reset to the initial state
        currentState = selectedOption;
        initialChoice = null;
        initState();  // Call initState to update the navbar row
    } else {
        
        // Handle sub-options behavior
        handleSubOption(selectedOption);
        currentState = selectedOption;
        initialChoice = selectedOption;
        initState();  // Call initState to update the navbar row
    }
}

function initState() {
    // Clear the current content of the navbar row
    const navbarRow = document.getElementById('navbarRow');
    navbarRow.innerHTML = '';

    // Add the selected option and initial choice to the navbar row
    const selectedOptionElement = document.createElement('div');
    selectedOptionElement.classList.add('col');
    navbarRow.appendChild(selectedOptionElement);

    if (initialChoice) {
        const initialChoiceElement = document.createElement('div');
        initialChoiceElement.innerHTML = `<button onclick="showSubMenu('${initialChoice}')" class="btn btn-warning">${initialChoice}</button>`;
        initialChoiceElement.classList.add('col');
        navbarRow.appendChild(initialChoiceElement);
    }
}

function handleSubOption(subOption) {
    // Customize this function based on the desired behavior for sub-options
    switch (subOption) {
        case 'Display1':
            // Load content into the heroDiv for Display1
            loadContent('heroDiv');

            break;
        // Add more cases for other sub-options if needed
        case 'Display2':
            // Load content into the heroDiv for Display1
            loadContent('content');
            break;
        default:
            break;
    }
}

// function loadContent(contentFile) {
//     // Load content into the heroDiv based on the specified content file
//     const heroDiv = document.getElementById('heroDiv');
//     fetch(contentFile)
//         .then(response => response.text())
//         .then(data => {
//             heroDiv.innerHTML = data;
//         })
//         .catch(error => console.error('Error loading content:', error));
// }
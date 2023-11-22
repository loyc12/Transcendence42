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


let currentState = 'home';  // Initialize the current state to 'home'
let initialChoice = null;    // Keep track of the initial choice
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
        initialChoiceElement.innerHTML = `<button onclick="showSubMenu('${initialChoice}')"  class="button">${initialChoice}</button>`;
        initialChoiceElement.classList.add('col');
        navbarRow.appendChild(initialChoiceElement);
    }

    // Create a new set of sub-options
    const subOptions = generateSubOptions(currentState);

    // Add the new set of sub-option buttons to the navbar row
    subOptions.forEach((subOption, index) => {
        const subOptionElement = document.createElement('div');
        subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" class="button">${subOption}</button>`;
        subOptionElement.classList.add('col');
        navbarRow.appendChild(subOptionElement);
    });
}

function showSubMenu(selectedOption) {
    // Check if the selected option is to the left of the current state
    const selectedOptionIndex = ['home','info', 'remote', 'local', 'login'].indexOf(selectedOption);
    const currentStateIndex = ['home','info', 'remote', 'local', 'login'].indexOf(currentState);

   if (selectedOptionIndex < currentStateIndex) {
        // Reset to the initial state
        currentState = selectedOption;
        initialChoice = null;
        initState();  // Call initState to update the navbar row
    } else {
        
        // Handle sub-options behavior
        currentState = selectedOption;
        initialChoice = selectedOption;
        handleSubOption(selectedOption);
        initState();  // Call initState to update the navbar row
    }
}



function handleSubOption(subOption) {
    // Customize this function based on the desired behavior for sub-options
    switch (subOption) {
        case 'Display1':
            // Load content into the heroDiv for Display1
            loadContent('heroDiv');
            // loadContent('content1');

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

function loadContent(contentFile) {
    // Load content into the heroDiv based on the specified content file
    const heroDiv = document.getElementById('heroDiv');
    fetch(contentFile)
        .then(response => response.text())
        .then(data => {
            heroDiv.innerHTML = data;
        })
        .catch(error => console.error('Error loading content:', error));
}

function renderInitNavbar() {
    // Customize this function to render another navbar to the init value
    const navbarRow = document.getElementById('navbarRow');
    navbarRow.innerHTML = '';

    // Add the selected option and initial choice to the navbar row
    const selectedOptionElement = document.createElement('div');
    selectedOptionElement.classList.add('col');
    navbarRow.appendChild(selectedOptionElement);

    if (initialChoice) {
        const initialChoiceElement = document.createElement('div');
        initialChoiceElement.innerHTML = `<button onclick="showSubMenu('${initialChoice}')" class="button">${initialChoice}</button>`;
        initialChoiceElement.classList.add('col');
        navbarRow.appendChild(initialChoiceElement);
    }

    // Create a new set of sub-options
    const subOptions = generateSubOptions(currentState);

    // Add the new set of sub-option buttons to the navbar row
    subOptions.forEach((subOption, index) => {
        const subOptionElement = document.createElement('div');
        subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" class="button">${subOption}</button>`;
        subOptionElement.classList.add('col');
        navbarRow.appendChild(OptionElement);
    });
}

function generateSubOptions(selectedOption) {
    // You can customize this function to generate sub-options based on the selected option
    switch (selectedOption) {
        case 'home':
            return ['home','Info', 'Remote', 'Local', 'Login'];
        case 'Info':
            return ['home','Profile', 'Stats'];
        case 'Remote':
            return ['home','Match', 'Tournament'];
        case 'Local':
            return ['home','VS', 'AI', 'More'];
        case 'Login':
            return ['home'];
        default:
            return [];
    }
}
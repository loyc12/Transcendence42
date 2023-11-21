// Define modules and their corresponding content
const modules = {
    home: 'home.html',
    display: {
        Profile: 'profile.html',
        Stats: 'stats.html',
        Others: 'others.html'
    },
    game: {
        Solo: 'solo.html',
        Remote: 'remote.html',
        Tournament: 'tournament.html'
    },
    list: {
        Visitor: 'visitors.html',
        Leader: 'leaders.html',
        Match: 'matchs.html'
    }
};

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
buttonModule3.addEventListener('click', function () {select_hero_content(3);})

select_hero_content(0)

// integration of the navbar

let currentState = 'home';  // Initialize the current state to 'home'
let initialChoice = null;    // Keep track of the initial choice

// Function to initialize the navbar based on the current state
function initState() {
    const navbarRow = document.getElementById('navbarRow');
    navbarRow.innerHTML = '';

    // Create a button for the home option
    const homeButton = document.createElement('div');
    homeButton.innerHTML = '<button onclick="showSubMenu(\'home\')" class="btn btn-outline-primary">Home</button>';
    homeButton.classList.add('col');
    navbarRow.appendChild(homeButton);

    // Generate and append sub-option buttons
    const subOptions = generateSubOptions(currentState);
    subOptions.forEach(subOption => {
        const subOptionElement = document.createElement('div');
        subOptionElement.innerHTML = `<button onclick="handleSubOptionButtonClick('${subOption}')" class="btn btn-outline-primary">${subOption}</button>`;
        subOptionElement.classList.add('col');
        navbarRow.appendChild(subOptionElement);
    });


    // Add click event listener to the "forEach" button
    // const forEachButtonElement = document.getElementById('forEach');
    forEachButtonElement.addEventListener('click', () => handleSubOptionButtonClick(currentState));
}

function showSubMenu(selectedOption) {
    // Check if the selected option is to the left of the current state
    const selectedOptionIndex = ['home','display', 'game', 'list'].indexOf(selectedOption);
    const currentStateIndex = ['home','display', 'game', 'list'].indexOf(currentState);

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
        currentState = selectedOption;
        initialChoice = selectedOption;
        handleSubOption(selectedOption);
        initState();  // Call initState to update the navbar row
    }
}

function handleSubOptionButtonClick(subOption) {
    handleSubOption(subOption);
}

// Function to handle sub-options behavior
function handleSubOption(selectedOption) {
    const contentFile = modules[currentState][selectedOption];
    if (contentFile) {
        loadContent(contentFile);
    }
}

// Function to load content into the heroDiv
function loadContent(contentFile) {
    const heroDiv = document.getElementById('heroDiv');
    fetch(contentFile)
        .then(response => response.text())
        .then(data => {
            heroDiv.innerHTML = data;
        })
        .catch(error => console.error('Error loading content:', error));
}

// Generate and append sub-option buttons
function generateSubOptions(selectedOption) {
    // You can customize this function to generate sub-options based on the selected option
    switch (selectedOption) {
        case 'home':
            return ['Display', 'Game', 'List'];
        case 'display':
            return ['Profile', 'Stats', 'Others'];
        case 'game':
            return ['Solo', 'Remote', 'Tournament'];
        case 'list':
            return ['Visitor', 'Leader', 'Match'];
        default:
            return [];
    }
}

// Function to initialize the navbar based on the current state
// function initState() {
//     const navbarRow = document.getElementById('navbarRow');
//     navbarRow.innerHTML = '';

//     // Create a button for the home option
//     const homeButton = document.createElement('div');
//     homeButton.innerHTML = '<button onclick="showSubMenu(\'home\')" class="btn btn-outline-primary">Home</button>';
//     homeButton.classList.add('col');
//     navbarRow.appendChild(homeButton);

//     // Generate and append sub-option buttons
//     const subOptions = generateSubOptions(currentState);
//     subOptions.forEach(subOption => {
//         const subOptionElement = document.createElement('div');
//         subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" class="btn btn-outline-primary">${subOption}</button>`;
//         subOptionElement.classList.add('col');
//         navbarRow.appendChild(subOptionElement);
//     });
// }
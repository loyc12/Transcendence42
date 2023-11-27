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
        // handleSubOption(selectedOption);
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
        case 'home':
            // Load content into the heroDiv for Display1
            loadContent('heroDiv');

            break;
            
        case 'info':
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
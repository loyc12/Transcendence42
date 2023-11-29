// // Load the navbar content
// let currentStateX = 'Home';  // Initialize the current state to 'home'
//     let initChoice = null;    // Keep track of the initial choice
//     function initState() {
//         // Clear the current content of the navbar row
//         const navbarRow = document.getElementById('NavBar');
//         navbarRow.innerHTML = '';

//         // Add the selected option and initial choice to the navbar row
//         const selectedOptionElement = document.createElement('div');
//         selectedOptionElement.classList.add('col');
//         navbarRow.appendChild(selectedOptionElement);

//         if (initChoice) {
//             const initChoiceElement = document.createElement('div');
//             initChoiceElement.innerHTML = `<button onclick="showSubMenu('${initChoice}')" id="NavBar" class="NavBar" class="button">${initChoice}</button>`;
//             initChoiceElement.classList.add('col');
//             navbarRow.appendChild(initChoiceElement);
//         }

//         // Create a new set of sub-options
//         const subOptions = generateSubOptions(currentStateX);

//         // Add the new set of sub-option buttons to the navbar row
//         subOptions.forEach((subOption, index) => {
//             const subOptionElement = document.createElement('div');
//             subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" id="NavBar" class="NavBar" class="button">${subOption}</button>`;
//             subOptionElement.classList.add('col');
//             navbarRow.appendChild(subOptionElement);
//         });
//     }

//     function showSubMenu(selectedOption) {
//             // Check if the selected option is to the left of the current state
//             const selectedOptionIndex = ['Home','Info', 'Game', 'Login'].indexOf(selectedOption);
//             const currentStateIndex = ['Home','Info', 'Game', 'Login'].indexOf(currentStateX);

//         if (selectedOptionIndex < currentStateIndex) {
//             // Reset to the initial state
//             currentStateX = selectedOption;
//             initChoice = null;
//             initState();  // Call initState to update the navbar row
//         } else {
            
//             // Handle sub-options behavior
//             currentStateX = selectedOption;
//             initChoice = selectedOption;
//             initState();  // Call initState to update the navbar row
//             handleSubOption(selectedOption);
//         }
//     }

//     function handleSubOption(subOption) {
//         // Customize this function based on the desired behavior for sub-options
//         switch (subOption) {
//             case 'Home':
//                 // Load content into the heroDiv for Display1
//                 loadContent('HeroDiv');            // loadContent('content1');
//                 break;
//                         // Add more cases for other sub-options if needed
//             case 'Info':
//                 // Load content into the heroDiv for Display1
//                 loadContent('content');
//                 break;
//             default:
//                 break;
//         }
//     }
    

//     function loadContent(contentFile) {
//         // Load content into the heroDiv based on the specified content file
//         const heroDiv = document.getElementById('heroDiv');
//         fetch(contentFile)
//             .then(response => response.text())
//             .then(data => {
//                 heroDiv.innerHTML = data;
//             })
//             .catch(error => console.error('Error loading content:', error));
//     }

//     function renderInitNavbar() {
//         // Customize this function to render another navbar to the init value
//         const navbarRow = document.getElementById('NavBar');
//         navbarRow.innerHTML = '';

//         // Add the selected option and initial choice to the navbar row
//         const selectedOptionElement = document.createElement('div');
//         selectedOptionElement.classList.add('col');
//         navbarRow.appendChild(selectedOptionElement);

//         if (initChoice) {
//             const initChoiceElement = document.createElement('div');
//             initChoiceElement.innerHTML = `<button onclick="showSubMenu('${initChoice}') "id="NavBar" class="NavBar" class="button">${initChoice}</button>`;
//             initChoiceElement.classList.add('col');
//             navbarRow.appendChild(initChoiceElement);
//         }

//         // Create a new set of sub-options
//         const subOptions = generateSubOptions(currentStateX);

//         // Add the new set of sub-option buttons to the navbar row
//         subOptions.forEach((subOption, index) => {
//             const subOptionElement = document.createElement('div');
//             subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" id="NavBar" class="NavBar" class="button">${subOption}</button>`;
//             subOptionElement.classList.add('col');
//             navbarRow.appendChild(OptionElement);
//         });
//     }

// function generateSubOptions(selectedOption) {
//     // You can customize this function to generate sub-options based on the selected option
//     switch (selectedOption) {
//         case 'Home':
//             return ['Home','Info', 'Game',  'Login'];
//         case 'Info':
//             return ['Home','Info', 'Game',  'Login'];
//         case 'Game':
//             return ['Home','Tournament', 'Freeplay', 'TwoPlaye', 'OnePlayer'];
//         case 'Tournament':
//             return ['Home','Pingest', 'Pinger', 'Ping', 'Random', 'Pong', 'Ponger', 'Pongest'];
//         case 'Freeplay':
//             return ['Home','Pingest', 'Pinger', 'Ping', 'Random', 'Pong', 'Ponger', 'Pongest'];
//         case 'TwoPlayer':
//             return ['Home','Pingest', 'Pinger', 'Ping', 'Random', 'Pong', 'Ponger', 'Pongest'];
//         case 'OnePlayer':
//             return ['Home','Pingest', 'Pinger', 'Ping', 'Random', 'Pong', 'Ponger', 'Pongest'];
//         case 'Login':
//             return ['Home','Info', 'Game',  'Login'];
//         default:
//             return [];
//     }
// }




// let currentState = 'home';  // Initialize the current state to 'home'
// let initChoice = null;    // Keep track of the initial choice
// function initState() {
    //     // Clear the current content of the navbar row
    //     const navbarRow = document.getElementById('navbarRow');
    //     navbarRow.innerHTML = '';

    //     // Add the selected option and initial choice to the navbar row
    //     const selectedOptionElement = document.createElement('div');
    //     selectedOptionElement.classList.add('col');
    //     navbarRow.appendChild(selectedOptionElement);

    //     if (initChoice) {
    //         const initChoiceElement = document.createElement('div');
    //         initChoiceElement.innerHTML = `<button onclick="showSubMenu('${initChoice}')" class="btn btn-warning">${initChoice}</button>`;
    //         initChoiceElement.classList.add('col');
    //         navbarRow.appendChild(initChoiceElement);
    //     }

    //     // Create a new set of sub-options
    //     const subOptions = generateSubOptions(currentState);

    //     // Add the new set of sub-option buttons to the navbar row
    //     subOptions.forEach((subOption, index) => {
    //         const subOptionElement = document.createElement('div');
    //         subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" class="btn btn-secondary">${subOption}</button>`;
    //         subOptionElement.classList.add('col');
    //         navbarRow.appendChild(subOptionElement);
    //     });
// }

// function showSubMenu(selectedOption) {
    //         // Check if the selected option is to the left of the current state
    //         const selectedOptionIndex = ['home','display', 'game', 'option'].indexOf(selectedOption);
    //         const currentStateIndex = ['home','display', 'game', 'option'].indexOf(currentState);

    //         if (selectedOption === 'home') {
    //             // Handle the 'Home' option
    //             if (currentState !== 'home') {
    //                 currentState = 'home';
    //                 initChoice = null;
    //                 initState();  // Call initState to update the navbar row
    //             }
    //         } else if (selectedOptionIndex < currentStateIndex) {
    //             // Reset to the initial state
    //             currentState = selectedOption;
    //             initChoice = null;
    //             initState();  // Call initState to update the navbar row
    //         } else {
                
    //             // Handle sub-options behavior
    //             currentState = selectedOption;
    //             initChoice = selectedOption;
    //             handleSubOption(selectedOption);
    //             initState();  // Call initState to update the navbar row
    //         }
// }

// function handleSubOption(subOption) {
    //     // Customize this function based on the desired behavior for sub-options
    //     switch (subOption) {
    //         case 'Display1':
    //             // Load content into the heroDiv for Display1
    //             loadContent('Logo/logo2.html');
                
    //             break;
    //             // Add more cases for other sub-options if needed
    //             case 'Display2':
    //                 // Load content into the heroDiv for Display1
    //                 loadContent('logo');
    //             break;
    //         default:
    //             break;
    //     }
// }

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

// function renderInitNavbar() {
    //     // Customize this function to render another navbar to the init value
    //     const navbarRow = document.getElementById('navbarRow');
    //     navbarRow.innerHTML = '';

    //     // Add the selected option and initial choice to the navbar row
    //     const selectedOptionElement = document.createElement('div');
    //     selectedOptionElement.classList.add('col');
    //     navbarRow.appendChild(selectedOptionElement);

    //     if (initChoice) {
    //         const initChoiceElement = document.createElement('div');
    //         initChoiceElement.innerHTML = `<button onclick="showSubMenu('${initChoice}')" class="btn btn-warning">${initChoice}</button>`;
    //         initChoiceElement.classList.add('col');
    //         navbarRow.appendChild(initChoiceElement);
    //     }

    //     // Create a new set of sub-options
    //     const subOptions = generateSubOptions(currentState);

    //     // Add the new set of sub-option buttons to the navbar row
    //     subOptions.forEach((subOption, index) => {
    //         const subOptionElement = document.createElement('div');
    //         subOptionElement.innerHTML = `<button onclick="showSubMenu('${subOption}')" class="btn btn-primary">${subOption}</button>`;
    //         subOptionElement.classList.add('col');
    //         navbarRow.appendChild(OptionElement);
    //     });
// }

// function generateSubOptions(selectedOption) {
    //     // You can customize this function to generate sub-options based on the selected option
    //     switch (selectedOption) {
    //         case 'home':
    //             return ['home','Display', 'Game', 'Option'];
    //         case 'display':
    //             return ['home','Display1', 'Display2', 'Display3'];
    //         case 'game':
    //             return ['home','Game1', 'Game2', 'Game3'];
    //         case 'option':
    //             return ['home','Option1', 'Option2', 'Option3'];
    //         default:
    //             return [];
    //     }
// }


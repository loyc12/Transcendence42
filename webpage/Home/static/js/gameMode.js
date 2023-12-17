
// Variable to store selected options
let selectedOptions = {};

let full_game_page_states_list = ['gameMode', 'gameTypeLocal', 'gameTypeOnline', 'lobby', 'game', 'aftergame', 'tournament']
// Function to load a module
function loadModule(moduleName) {

    console.log('Entered ladModule with moduleName : ' + moduleName)
    // Flush all submodule content
    for (c of full_game_page_states_list) {
        console.log('Trying to hide ' + c + ' module display.')
        document.getElementById(c).style.display = 'none'
    }

    // Select desired submodule
    console.log('requested Module name : ' + moduleName)
    if (moduleName === 'gameMode') {
        console.log('Load base gameMode page')
        document.getElementById('gameMode').style.display = 'block';
    }
    else if (moduleName === 'local')
    {
        console.log('Load gameTypeLocal module')
        document.getElementById('gameTypeLocal').style.display = 'block';
    }
    else if (moduleName === 'online') {
        console.log('Load gameTypeOnline module')
        document.getElementById('gameTypeOnline').style.display = 'block';
    }
    else if (moduleName === 'lobby') {
        console.log('Load lobby')
        document.getElementById('lobby').style.display = 'block';
    }
    else if (moduleName === 'game') {
        console.log('Load game')
        document.getElementById('game').style.display = 'block';
    }
    else if (moduleName === 'aftergame') {
        console.log('Load aftergame')
        document.getElementById('aftergame').style.display = 'block';
    }
    // else if (moduleName === 'tournament') {
    //     console.log('Load tournament')
    //     document.getElementById('tournament').style.display = 'block';
    // }
    else {
        console.log('Make join game request.')
        request_join_game(moduleName)
    }
        //case 'module1':
        //    moduleContainer.innerHTML = `
        //        <button onclick="loadSubModule('subModule1')">Game Local: SOLO [AI]</button>
        //        <button onclick="loadSubModule('subModule2')">Game Local: 1 Vs 1 </button>
        //    `;
        //    break;
        //case 'module2':
        //    moduleContainer.innerHTML = `
        //        <button onclick="loadSubModule('subModule3')">Game Online: Tournament </button>
        //        <button onclick="loadSubModule('subModule4')">Game Online: MultiPlayer </button>
        //    `;
        //    break;
        //default:
        //    break;
    //}
}

// Function to load a sub-module
function loadSubModule(subModuleName) {
    // Assuming you want to store the selected sub-module in the variable
    selectedOptions.subModule = subModuleName;

    // Display the result or take further actions
    console.log('Selected Options:', selectedOptions);
}

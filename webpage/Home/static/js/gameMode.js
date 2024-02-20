
// Variable to store selected options
let selectedOptions = {};

let full_game_page_states_list = ['gameMode', 'gameTypeLocal', 'gameTypeOnline', 'lobby', 'game', 'aftergame']
// Function to load a module
function loadModule(moduleName) {

    // Flush all submodule content
    for (c of full_game_page_states_list) {
        document.getElementById(c).style.display = 'none'
    }
    // Select desired submodule
    if (moduleName === 'gameMode') {
        document.getElementById('gameMode').style.display = 'block';
    }
    else if (moduleName === 'local')
    {
        document.getElementById('gameTypeLocal').style.display = 'block';
    }
    else if (moduleName === 'online') {
        document.getElementById('gameTypeOnline').style.display = 'block';
    }
    else if (moduleName === 'lobby') {
        document.getElementById('lobby').style.display = 'block';
        if (isTournament)
        {
            document.getElementById('tournament').style.display = 'block';
            if (isGhostLobby)
            {
                document.getElementById('tournament').style.display = 'block';
            }
        }
        else{
            document.getElementById('tournament').style.display = 'block';
        }
    }
    else if (moduleName === 'game') {
        document.getElementById('game').style.display = 'block';
    }
    else if (moduleName === 'aftergame' ) {
        if (isTournament)
            isGhostLobby = true;
        document.getElementById('aftergame').style.display = 'block';
    }
    else if (moduleName == 'help')
    {
        //console.log('WARNING : unimplemented call to loadModule for help')
    }
    else {
        console.log('Make join game request.')
        request_join_game(moduleName)
    }
}

// Function to load a sub-module
function loadSubModule(subModuleName) {
    // Assuming you want to store the selected sub-module in the variable
    selectedOptions.subModule = subModuleName;

    // Display the result or take further actions
    console.log('Selected Options:', selectedOptions);
}

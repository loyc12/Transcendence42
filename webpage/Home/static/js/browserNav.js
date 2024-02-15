
let currrentState = 'init';


function goBackAndRemoveLast() {
    console.log('--- goBack CALL ---');
    // console.log(navigationState);
    // Check if there are states to go back to
    if (navigationState.length > 1) {
        // Remove the last state from your custom stack
        navigationState.pop();  
    }
    // Use history.back() to navigate back one step
    history.back();

    console.log('--- removeLast CALL ---');
    console.log(history);
  }

window.onpopstate = function (event) {
    console.log('--- onpopstate ---');

    if (event.state) {
        console.log('[***] THIS IS BROWSER EVENT  onpopstate --: event.state ', event.state);
        goBackAndRemoveLast();
        
        currrentState = event.state;
        console.log('___  call handleStateChange\n ___currentState  ', currrentState);
        handleStateChange(currrentState);
        goBackAndRemoveLast();
    }
    else {

        console.log('[###]  onpopstate NO event.state location.hash ::', location.hash);
        handleStateChange(location.hash);
    }

};

function setupBeforeUnload() {
    window.onbeforeunload = function() {
        fetch_user_logout()
        disconnect_socket();
        disconnect_tour_socket();
        wipe_tournament_data();
        disconnect_user_socket();
    };
}

window.onload = function (event) {
    if (event.state == 'init' && location.hash != event.state) {
        console.log('___ ---event.state =', event.state, ' location.hash = ', location.hash);
        event.state = 'init';
    }
    console.log(' --- onload handleChange --- : ', event.state);
    handleStateChange(event.state);
    
    setupBeforeUnload();
};


window.addEventListener('popstate', function(event) {

    console.log('--- addEventListener --- popstate ---');
    if (event.state != null) {
        console.log('\t __ popstate handleStateChange __', event.state);
        // new add a simili-global function to set state of history
        pushStateAndUpdate(event.state, event.state);
        handleStateChange(event.state);
    }
    else {

        console.log('\t__ popstate __ event.state IS NULL  ___');
        console.log('__ LOCATION is NOT SET ___ location.hash >>', this.location.hash);
    }
});


addEventListener("beforeunload", (event) => {});

onbeforeunload = (event) => {};


function handleStateChange(newState) {

    console.log(' ---  handleStateChange  ---   <<>> ', newState);
    // console.log("** [] [] navigationState [] []: ", navigationState);

    if (newState === 'lobby'  || newState === 'aftergame'|| newState === 'tournament') {
        console.log('----handleStateChange == select_hero_content >> INIT');
        select_hero_content('init');
    }
    else if (newState === 'info')
        select_hero_content('info');
    else if (newState === 'help')
        select_hero_content('help');
    else if (newState === 'gameMode')
        select_hero_content('gameMode');
    else if (newState === 'game')
        select_hero_content('game');
    else if (newState === 'gameTypeLocal')
       select_hero_content('gameTypeLocal');
    else if (newState === 'gameTypeOnline')
      select_hero_content('gameOnline');
    else
      select_hero_content('init');
}
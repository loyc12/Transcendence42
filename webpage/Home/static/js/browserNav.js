
let currrentState = 'init';
let stateID = 0;


function goBackAndRemoveLast() {
    console.log('--- goBack CALL ---');
    // console.log(navigationState);
    // Check if there are states to go back to
    if (navigationState.length > 1) {
        // Remove the last state from your custom stack
        console.log("REMOVING LAST STATE FROM NAV ! ");
        navigationState.pop();  
    }
    // Use history.back() to navigate back one step
    history.back();

    console.log('--- removeLast CALL ---');
    console.log(history);
  }

// window.onpopstate = function (event) {
//     console.log('--- onpopstate ---');

//     if (event.state) {
//         console.log('[***] THIS IS BROWSER EVENT  onpopstate --: event.state ', event.state);
//         goBackAndRemoveLast();
        
//         currrentState = event.state;
//         console.log('___  call handleStateChange\n ___currentState  ', currrentState);
//         handleStateChange(currrentState);
//         goBackAndRemoveLast();
//     }
//     else {

//         console.log('[###]  onpopstate NO event.state location.hash ::', location.hash);
//         handleStateChange(location.hash);
//     }
// };

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

    var pstate = event.state;
    console.log('--- addEventListener --- popstate --- location : ' + pstate);

	
    if (pstate != null) {
        // loadBodyContent(location,false);
        var id = pstate.id;
        var state = pstate.state;
        //var popedState = history.length;
        console.log('--- addEventListener :: state : ' + state);
        console.log('--- addEventListener :: id : ' + id);
        if (id < stateID) {
            // Backward button was pressed
            console.log("Backward button was pressed");
            window.history.go(-1);
            var newPState = history.state;
            console.log("newPState : " + newPState);
            if (newPState == null)
            {
                console.log("newPState IS NULL");
                return;
            }
            state = newPState.state;
            stateID = newPState.id;
            console.log("loading new state " + state);
            console.log("With stateID " + stateID);

            handleStateChange(state);
        }
        else {
            // Forward button was pressed
            console.log("Forward button was pressed");
            console.log("received id vs stateID : " + id + " vs " + stateID);
            window.history.go(1);
            var newPState = history.state;
            if (newPState == null)
                return;
            state = newPState.state;
            stateID = newPState.id;
            console.log("newPState : " + newPState);
            handleStateChange(state);
        }

    } else {
        //window.history.back();
    }
    // if (event.state != null) {
    //     console.log('\t __ popstate handleStateChange __', event.state);
    //     // new add a simili-global function to set state of history
    //     pushStateAndUpdate(event.state, event.state);
    //     handleStateChange(event.state);
    // }
    // else {

    //     console.log('\t__ popstate __ event.state IS NULL  ___');
    //     console.log('__ LOCATION is NOT SET ___ location.hash >>', this.location.hash);
    // }
});


addEventListener("beforeunload", (event) => {});

onbeforeunload = (event) => {};


function handleStateChange(newState) {

    console.log(' ---  handleStateChange  ---   <<>> ', newState);
    // console.log("** [] [] navigationState [] []: ", navigationState);

    if (newState === 'lobby'  || newState === 'aftergame'|| newState === 'tournament') {
        console.log('----handleStateChange == select_hero_content >> INIT');
        select_hero_content('init', doPushState=false);
    }
    else if (newState === 'info')
        select_hero_content('info', doPushState=false);
    else if (newState === 'help')
        select_hero_content('help', doPushState=false);
    else if (newState === 'gameMode')
        select_hero_content('gameMode', doPushState=false);
    else if (newState === 'game')
        select_hero_content('game', doPushState=false);
    else if (newState === 'gameTypeLocal')
       select_hero_content('gameTypeLocal', doPushState=false);
    else if (newState === 'gameTypeOnline')
      select_hero_content('gameOnline', doPushState=false);
    else
      select_hero_content('init', doPushState=false);
}
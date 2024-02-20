
let currrentState = 'init';
let stateID = 0;


function setupBeforeUnload() {
    window.onbeforeunload = function() {
        fetch_user_logout()
        disconnect_socket();
        disconnect_tour_socket();
        wipe_tournament_data();
        disconnect_user_socket();
    };
}

const onLoadHistoryState = {'state': 'root', 'id': 0};

window.onload = function (event) {
    if (event.state == 'init' && location.hash != event.state) {
        console.log('___ ---event.state =', event.state, ' location.hash = ', location.hash);
        event.state = 'init';
    }
    console.log(' --- onload handleChange --- : ', event.state);
    //handleStateChange(event.state);

    setupBeforeUnload();
    window.removeEventListener('popstate', _handleBackAndForwardEvent)
    window.history.pushState(onLoadHistoryState, "", null);
    window.addEventListener('popstate', _handleBackAndForwardEvent);

    // Adds init state to history.
    select_hero_content('init');
};


let _handleBackAndForwardEvent = function (event) {

    var pstate = event.state;
    console.log('--- addEventListener --- popstate --- location : ' + pstate);

    if (pstate != null) {
        var id = pstate.id;
        var state = pstate.state;
        console.log('--- addEventListener :: state : ' + state);
        console.log('--- addEventListener :: id : ' + id);
        if (state == 'root') {
            console.log('event state == root !!');
            window.history.back();
        }
        if (id < stateID) {
            // Backward button was pressed
            console.log("Backward button was pressed");
            console.log("received id vs stateID : " + id + " vs " + stateID);
            // state = newPState.state;
            stateID = id;
            console.log("loading new state " + state);
            // console.log("With stateID " + stateID);
            // if (state == 'game')
            //     window.history.go(-1);

            handleStateChange(state);
        }
        else if (id > stateID) {
            // Forward button was pressed
            console.log("Forward button was pressed");
            console.log("received id vs stateID : " + id + " vs " + stateID);
            stateID = id;
            console.log("With stateID " + stateID);

            handleStateChange(state);
        }
        //else {
        //    console.log("onpopstate :: travelled to same state.");
        //    console.log("received id vs stateID : " + id + " vs " + stateID);
        //}
    } else {
        window.history.back();
    }
}


function handleStateChange(newState) {

    console.log(' ---  handleStateChange  ---   <<>> ', newState);

    if (newState === 'lobby'  || newState === 'aftergame'|| newState === 'tournament') {
        console.log('----handleStateChange == select_hero_content >> INIT');
        select_hero_content('init', doPushState=false);
    }
    else if (newState === 'login' && user_id  == null)
        select_hero_content('login', doPushState=false);
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

let currrentState = 'init';

// const routes = [
//     { path: '#init', component: 'init' },
//     { path: '#help', component: 'help' },
//     { path: '#info', component: 'info' },
//     { path: '#game', component: 'game' },
//   ];




window.onpopstate = function (event) {
    console.log('--- onpopstate ---');

    if (event.state) {
        console.log('[***] THIS IS BROWSER EVENT  onpopstate: ', event.state);
        currrentState = event.state;
        // location.hash = currrentState;
        // console.log('[***] LOCATION HASH  ', location.hash);
        handleStateChange(currrentState);
    }
    else {

        console.log('[###] THIS BROWSER EVENT  onpopstate ELSE ');
        handleStateChange(currrentState);
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
    
    //history.pushState(newStack, newState);
    
    console.log('@@@ onload part of the prog and event.state is : ', event.state);
    handleStateChange(event.state);
    
    setupBeforeUnload();
};

window.addEventListener('popstate', function(event) {

    console.log('--- addEventListener --- popstate ---');

    if (event.state != null) {
        console.log('__ LOCATION is SET to ::', event.state);
    
        //// history.pushState(localStorage, event.state );
        // new add a simili-global function to set state of history
        // pushStateAndUpdate(event.state, event.state);
        handleStateChange(event.state);
    }
    else {

        console.log('__ LOCATION is NOT SET ___ ');
        console.log("** [] [] browserNav VALUE navigationState [] []: ", navigationState);
        window.history.back();
    }
});

addEventListener("beforeunload", (event) => {});

onbeforeunload = (event) => {};


function handleStateChange(newState) {

    console.log(' ---  handleStateChange  ---  Change to <<>> ', newState);
    // console.log('&&& Hash Change:', location.hash);

    if (newState === 'lobby' || newState === 'game' || newState === 'aftergame'|| newState === 'tournament') {
        select_hero_content('init');
    }
    else if (newState === 'info')
        select_hero_content('info');
    else if (newState === 'help')
        select_hero_content('help');
    else if (newState === 'gameMode')
        select_hero_content('gameMode');
    else if (newState === 'gameTypeLocal')
       select_hero_content('gameTypeLocal');
    else if (newState === 'gameTypeOnline')
      select_hero_content('gameOnline');
    else
      select_hero_content('init');
}
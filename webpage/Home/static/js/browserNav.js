
let currrentState = 'init';

window.onpopstate = function (event) {
    if (event.state) {
        console.log('[***] THIS IS BROWSER EVENT STATE onpopstate: ', event.state);
        handleStateChange(event.state);
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
    console.log('{***} THIS IS BROWSER EVENT STATE onload: ', event);
    setupBeforeUnload()
};

addEventListener("beforeunload", (event) => {});
onbeforeunload = (event) => {};


function navigateForward(newState) {
    console.log('*** THIS IS BROWSER EVENT STATE navigateForward: ', newState);
    history.forward();
}


function handleStateChange(newState) {
    console.log('Navigated to: ', newState);
    if (newState === 'lobby' || newState === 'game' || newState === 'aftergame'|| newState === 'tournament') {
        select_hero_content('init');
    }
    else if (newState === 'info')
        select_hero_content('info');
    else if (newState === 'gameMode')
        select_hero_content('gameMode');
    else if (newState === 'gameTypeLocal')
        select_hero_content('gameTypeLocal');
    else if (newState === 'gameTypeOnline')
        select_hero_content('gameOnline');
    else
        select_hero_content('init');
}

let currrentState = 'init';
const routes = [
    { path: '#init', component: 'init' },
    { path: '#help', component: 'help' },
    { path: '#info', component: 'info' },
    { path: '#game', component: 'game' },
  ];
  
  

window.onpopstate = function (event) {
    console.log('--- onpopstate ---');

    if (event.state) {
        console.log('[***] THIS IS BROWSER EVENT STATE onpopstate: ', event.state);
        // history.pushState(navStack, event.state );
        currrentState = event.state;
        // location.hash = currrentState;
        // console.log('[***] LOCATION HASH  ', location.hash);
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
    
    // console.log('<<< {{onload}} ** event.state **  >>> ', event);
    // Assuming newState is the state object representing the initial state
    var newState =  event ;
    
    // console.log('{***} THIS IS BROWSER EVENT STATE {{onload}} ** newState ** :: ', newState);

    //history.pushState(newStack, newState);

    // handleStateChange(newState);
    
    setupBeforeUnload();
};


addEventListener("beforeunload", (event) => {});

onbeforeunload = (event) => {};


function handleStateChange(newState) {

    // console.log('### newState ### Navigated to: ', newState);
    console.log(' ---  handleStateChange  ---  Change to <<>> ', newState);
    const hash = window.location.hash;
    console.log('&&& Hash Change:', hash);

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
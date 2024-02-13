
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
        // currrentState = event.state;
        history.pushState(location.hash, event.state );
        // location.hash = currrentState;
        console.log('[***] LOCATION HASH  ', location.hash);
        handleStateChange(currrentState);
    }
    else {

        console.log('[###] THIS BROWSER EVENT  onpopstate ELSE ');
        handleStateChange(currrentState);
    }
    // else if (event) {
    // }
   

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

window.addEventListener('popstate', function(e) {
    var location = e.state;

    if (location != null) {
        console.log('__ LOCATION is SET to ::', location);
        // console.log('__ LOCATION.state is equal to ::', window.location.state);
        history.pushState(location.hash, location );
        handleStateChange(location);
        // loadBodyContent(location,false);
        // $('.addedMenuNavBarItem').remove();

    }
    //  else {
    //     window.history.back();
    // }
});

addEventListener("beforeunload", (event) => {});

onbeforeunload = (event) => {};


function handleStateChange(newState) {

    // console.log('### newState ### Navigated to: ', newState);
    console.log(' ---  handleStateChange  ---  Change to <<>> ', newState);
    // window.location.hash = newState;
    console.log('&&& Hash Change:', location.hash);

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
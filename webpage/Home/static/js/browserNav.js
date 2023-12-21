
let currrentState = 'init';

window.onpopstate = function (event) {
    if (event.state) {
        console.log('THIS IS BROWSER EVENT STATE onpopstate: ', event.state);
        handleStateChange(event.state);
    }
};

function handleStateChange(newState) {
    console.log('Navigated to: ', newState);
    if (newState === 'init' || newState === 'lobby' || newState === 'game' || newState === 'aftergame'|| newState === 'tournament'
        || newState === 'gameMode' || newState === 'gameTypeLocal' || newState === 'gameTypeOnline') {
        select_hero_content('init');
    if (newState === 'info') {
        select_hero_content('info');
    }
    else {
        console.log('Unknown state: ', newState);
    }}
}
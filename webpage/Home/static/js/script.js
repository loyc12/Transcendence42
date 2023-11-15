// vanilla-script.js
console.log("Script loaded successfully!");


document.addEventListener('DOMContentLoaded', function () {
    var module1Content = '<div>Content for Module 1</div>';
    var module2Content = '<div>Content for Module 2</div>';
    var listContent = '<div>Content for ListAlt</div>';
    var HeroDiv = document.querySelector('.HeroDiv');
    var NavBar = document.querySelector('.NavBar');

    // Add click event listeners to NavBar links
    document.querySelector('.NavBar a[href="#module1"]').addEventListener('click', function () {
        HeroDiv.innerHTML = module1Content;
    });
    
    document.querySelector('.NavBar a[href="#module2"]').addEventListener('click', function () {
        HeroDiv.innerHTML = module2Content;
    });

    document.querySelector('.NavBar a[href="#listContent"]').addEventListener('click', function () {
        NavBar.innerHTML = listContent;
    });


    showModule('module1'); // Show the initial module
    
    // document.querySelector('.NavBar a[href="#module1"]').addEventListener('click', function (event) {
    //     event.preventDefault();
    //     showModule('module1');
    // });
    
    // document.querySelector('.NavBar a[href="#module2"]').addEventListener('click', function (event) {
    //     event.preventDefault();
    //     showModule('module2');
    // });
    
    // history.replaceState({}, document.title, window.location.pathname);
});

function showModule(moduleId) {
    // Hide all modules
    var modules = document.querySelectorAll('.HeroDiv');
    modules.forEach(function (module) {
        module.classList.remove('active');
        history.replaceState({}, document.title, window.location.pathname);
    });

    // Show the selected module
    document.getElementById(moduleId).classList.add('active');
}

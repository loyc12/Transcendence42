document.addEventListener('DOMContentLoaded', function () {
    showModule('module1'); // Show the initial module

    document.querySelector('.NavBar a[href="#module1"]').addEventListener('click', function (event) {
        event.preventDefault();
        showModule('module1');
    });

    document.querySelector('.NavBar a[href="#module2"]').addEventListener('click', function (event) {
        event.preventDefault();
        showModule('module2');
    });
});

function showModule(moduleId) {
    // Hide all modules
    var modules = document.querySelectorAll('.HeroDiv');
    modules.forEach(function (module) {
        module.classList.remove('active');
    });

    // Show the selected module
    document.getElementById(moduleId).classList.add('active');
}

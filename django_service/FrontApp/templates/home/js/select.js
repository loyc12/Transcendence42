function goToHome() {
    const userSelector = document.getElementById('userSelector');
    const selectedUser = userSelector.options[userSelector.selectedIndex].text;
    localStorage.setItem('selectedUser', selectedUser);
    window.location.href = 'home.html';
}

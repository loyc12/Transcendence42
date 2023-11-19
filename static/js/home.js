const selectedUser = localStorage.getItem('selectedUser');
document.getElementById('selectedUser').textContent = selectedUser;


function butter_event_engaged(){
    console.log('Butter Time ?')
    fetch('/home/title')
        .then(response => response.text())
        .then(htmlContent => {
            // Replace an existing div in the DOM with the new HTML content
            document.getElementById('butter').innerHTML = htmlContent;
            console.log('Butter Time !')
        })
        .catch(error => console.error('Error:', error));
}
document.getElementById("butterTrigger").onclick = butter_event_engaged;

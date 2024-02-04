
let get_text_from_readable_stream = async function(stream) {
  const reader = stream.getReader();
  const { value, done } = await reader.read();

  if (done) {
    console.log("The stream was already closed!");
  } else {
    console.log(value);
  }
  return 
}

let loading_profile = false;
let fetch_user_profile = function () {

  console.log('Inside fetch_user_profile()')
  if (loading_profile)
    return;
  loading_profile = true;
  fetch('https://' + window.location.host + '/users/profile/get')
  .then (data => {
    elem = document.getElementById('profile');
    
    data.text().then(text => {
        if (elem)
            elem.innerHTML = text;
    })
  })
  .catch(function (err) {
    console.log('fetch of user profil failed !');
    console.log(err);
  })
  loading_profile = false;
}
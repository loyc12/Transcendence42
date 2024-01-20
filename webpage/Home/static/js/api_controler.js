
let _build_api_request_path = function(key) {
    return 'https://' + window.location.host + '/game/api/move/' + key + '/';
}

let _https_api_request = async function (api_path) {
    return fetch(api_path, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "apiKey": api_key,
        }
    })
    .then (function(response) {
        return response.json()
      })
      .then (function(data) {
        if (data.status === 'failure')
          alert('API request failed because : \n\t - ' + data.reason)
        if (data.status === 'success') {
          console.log('Returned data from API request : ' + data);
          console.log('response status : ', data.status);
          console.log('response reason : ', data.reason);
          console.log('response apiKey : ', data.apiKey);
          return data;
        } else {
          console.error('_https_api_request call failed');
        }
      })
}


let _api_request_move = async function (api_path) {

    api_resp = await _https_api_request(api_path);
    console.log('api_resp : ' + api_resp);
  
    return api_resp;
  }
  

let api_controler = async function (key) {
    let req_path = _build_api_request_path(key);
    return await _api_request_move(req_path);
}

let copy_api_key_to_clipboard = function () {
    navigator.clipboard.writeText(api_key);
}
/*
* API wrapper
*/

var API = {
	send: function(url, method, data, onSuccess, onError) {
		url = API_endpoint + url;
		
		var authToken = JSON.parse(localStorage.getItem('token'));
		
		var headerConfig = {		
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
			   'Accept': 'application/json',
		};
		if (authToken.token) {
			headerConfig['Authorization'] = 'token ' + authToken.token;
		}
		
		var initData = { 
			method: method,
		   headers: new Headers(headerConfig),
		   //mode: 'no-cors',
		   //cache: 'default',
		   body: data
		 };
		console.log(initData);

		fetch(url, initData)
		.then(function(res) {
			return res.json();
		})
		.then(function(json) {
			onSuccess(json);
		})
		.catch(function(err) {
		    onError(err);
		});
	}
}
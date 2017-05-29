/*
* API wrapper
*/

var API = {
	send: function(url, method, data, onSuccess, onError) {
		url = API_endpoint + url;

		var initData = { 
			method: method,
		   headers: new Headers({		
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
			   'Accept': 'application/json'
		   }),
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
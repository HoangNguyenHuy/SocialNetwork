/*
* API wrapper
*/

var API = {
	send: function(url, method, data, onSuccess, onError) {
		url = API_endpoint + url;

		var authToken = false;
		try {
		    authToken = JSON.parse(localStorage.getItem('token'));
		} catch(e) {}
		
		var headerConfig = {
//		      'Content-type': "application/x-www-form-urlencoded; charset=UTF-8",
			  'Accept': 'application/json',
		};
		if (method.toLowerCase() !== 'get' && data) {

            if (Object.prototype.toString.call(data) !== '[object FormData]') {
                headerConfig['Content-type'] = 'application/json; charset=utf-8';
                data = JSON.stringify(data);
            }

        }
		if (authToken) {
			headerConfig['Authorization'] = 'token ' + authToken.token;
		}
		
		var initData = { 
			method: method,
		   headers: new Headers(headerConfig),
		   //mode: 'no-cors',
		   //cache: 'default',
		   body: data
		 };
//		console.log(initData);

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
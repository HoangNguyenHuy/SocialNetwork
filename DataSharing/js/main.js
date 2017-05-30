var API_endpoint = "http://127.0.0.1:8080/api/v1/";



// clear all the local storage- Logout
$('#clear').click( function() {
window.localStorage.clear();
location = 'index.html';
return false;
});

$("#target").submit(function(e) {
	e.preventDefault();
	var form_data = $(this).serialize();
	
	API.send('post', 'post', form_data, function(res) {
		// Success reponse handle
		console.log(res);
		//localStorage.setItem('token', res.token);
		window.location = 'file.html';
	}, function(err){
		// Error handle		
		console.log(err);
	});
	
});

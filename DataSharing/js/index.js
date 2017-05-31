var API_endpoint = "http://127.0.0.1:8080/api/v1/";


$('.toggle').on('click', function() {
  $('.container').stop().addClass('active');
});

$('.close').on('click', function() {
  $('.container').stop().removeClass('active');
});



$("#form_login").submit(function(e) {
	e.preventDefault();
	var form_data = $(this).serialize();
	
	API.send('auth', 'post', form_data, function(res) {
		// Success reponse handle
		console.log(res);
		window.localStorage.setItem('token', res.token);
		var x = localStorage.getItem('token');
        if (x !== 'undefined') {
		    window.location = 'main.html';}
	}, function(err){
	    window.location = 'index.html';
		// Error handle		
	});
	
});

var API_endpoint = "http://127.0.0.1:8000/api/v1/";


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
		localStorage.setItem('token', res.token);
		window.location = 'main.html';
	}, function(err){
		// Error handle		
	});
	
});

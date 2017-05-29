var API_endpoint = "http://127.0.0.25:8014/api/v1/";


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
		window.location = '/home/hoangnguyen/workspace/SocialNetwork/SocialNetwork/DoAn/index.html';
	}, function(err){
		// Error handle		
	});
	
});

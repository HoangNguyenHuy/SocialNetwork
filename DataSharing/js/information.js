var API_endpoint = "http://127.0.0.1:8080/api/v1/";

$(window).load(function(){
	loadInformationUser();
});


//$(window).load(function(){
//	loadInformationUser();
//	$('#inputUser').val(item.username);
//});

function loadInformationUser(item) {
	console.log('Load Information User');
	API.send('user/11', 'get', null, function(res) {
		// Success reponse handle
		$('#username').val(res.username);
		$('#dob').val(res.dob);
		$('#first_name').val(res.first_name);
		$('#last_name').val(res.last_name);
		$('#phone').val(res.phone);
		$('#password').val(res.password);
		$('#email').val(res.email);
	}, function(err){
       // Error handle
	});
}

$('#upload_infor').submit(function (e){
    e.preventDefault();
	var form_data = $(this).serialize();
console.log(form_data);
//	API.send('user/11', 'put', form_data, function(res) {
//	    //success
////	    res.username = document.getElementById("username").value;
////	    res.dob = document.getElementById("dob").value;
////	    res.first_name = document.getElementById("first_name").value;
////	    res.last_name = document.getElementById("last_name").value;
////	    res.phone = document.getElementById("phone").value;
////	    res.password = document.getElementById("password").value;
////	    res.email = document.getElementById("email").value;
//	    console.log(res);
//	}, function(err){
//        // Error handle
//	});
})
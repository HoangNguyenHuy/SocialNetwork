var API_endpoint = "http://127.0.0.1:8080/api/v1/";

$(window).load(function(){
	loadInformationUser();
});


//$(window).load(function(){
//	loadInformationUser();
//	$('#inputUser').val(item.username);
//});

function loadInformationUser(item) {
    token = JSON.parse(localStorage.getItem("token"));
	console.log('Load Information User');
	API.send('user/'+token.user_id, 'get', null, function(res) {
		// Success reponse handle
		$('#username').val(res.username);
		$('#dob').val(res.dob);
		$('#first_name').val(res.first_name);
		$('#last_name').val(res.last_name);
		$('#phone').val(res.phone);
		$('#email').val(res.email);
	}, function(err){
       // Error handle
	});
}

$('#upload_infor').submit(function (e){
    e.preventDefault();
    var form_data ={}
    if (document.getElementById("email").value){
        form_data ={email: document.getElementById("email").value,}
    }
    if (document.getElementById("dob").value){
        form_data ={dob: document.getElementById("dob").value,}
    }
    if (document.getElementById("first_name").value){
        form_data ={first_name: document.getElementById("first_name").value,}
    }
    if (document.getElementById("last_name").value){
        form_data ={last_name: document.getElementById("last_name").value,}
    }
    if (document.getElementById("phone").value){
        form_data ={phone: document.getElementById("phone").value,}
    }
	API.send('user/'+token.user_id, 'put', form_data, function(res) {
	    //success
	    console.log(res);
	}, function(err){
        // Error handle
	});
})
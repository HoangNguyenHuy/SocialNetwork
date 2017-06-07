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
    console.log(form_data);
//	API.send('user/'+token.user_id, 'put', form_data, function(res) {
//	    //success
//	    console.log(res);
//	}, function(err){
//        // Error handle
//	});
})

$('#form_change_pass').submit(function (e){
    e.preventDefault();
    var newpass = document.getElementById("passnew").value;
    var confirm_pass= document.getElementById("passconfirm").value;
    if (newpass != confirm_pass){
//        $('#box_passconfirm').append('<img src="image/error.png" style="margin-top:5px;" width="20px" height="20px">');
            document.getElementById("confirm").innerHTML = '<img src="image/error.png" style="margin-top:5px;" width="20px" height="20px">'
    }
    else{
        document.getElementById("confirm").innerHTML = ''
        if (ValidCaptcha()==false){document.getElementById("error_message").innerHTML = 'Mã xác nhận không hợp lệ.'}
        else{
            document.getElementById("error_message").innerHTML = ''
            var form_data ={
        password : newpass,
        confirm_password : confirm_pass,
        }

        console.log(form_data);
        	API.send('user/change_password', 'put', form_data, function(res) {
        	    //success
        	}, function(err){
                // Error handle
        	});
        	alert("Đổi mật khẩu thành công !");
        	location.reload(true);
        }

    }
})

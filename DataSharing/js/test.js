var API_endpoint = "http://127.0.0.1:8080/api/v1/";

//function load_page() {
////    window.location.assign(window.location.href);
//    location.reload(true);
//}

$(window).load(function(){
    var x = localStorage.getItem('token');
//    console.log(x);
    if (x === null) {
    window.location = 'index.html';
    // localStorage not defined
}
});

// clear all the local storage- Logout
$('#clear').click( function() {
localStorage.clear();
console.log(window.localStorage.getItem('token'));
window.location = 'index.html';
return false;
});


$('#target').submit(function(e) {
	e.preventDefault();
	var form_data = {
	    content: $(this).find("[id='content']").val(),
	}

	API.send('post','post', form_data, function(res) {
		// Success reponse handle
		location.reload(true);
	}, function(err){
		// Error handle
	});
});


$('#targets').submit(function(e) {
	e.preventDefault();
	var form_data = new FormData(this);
	form_data.append('file', $(this).find("[id='targets_file_input']").val());

	API.send('data','post', form_data, function(res) {
		// Success reponse handle
//		console.log(res);
        location.reload(true);
	}, function(err){
		// Error handle
	});
});


$("#targets_file_input").on('change', function(e) {

//    console.log((this).files);
    handlePreviewUpload(this.files);
});


function handlePreviewUpload(files) {
//    console.log(files);
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var imageType = /^image\//;

        if (!imageType.test(file.type)) {
          continue;
        }

        var img = document.createElement("img");
        img.classList.add("preview-img");
        img.file = file;
        $("#upload_preview").append(img); // Assuming that "preview" is the div output where the content will be displayed.

        var reader = new FileReader();
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
        reader.readAsDataURL(file);
  }
}

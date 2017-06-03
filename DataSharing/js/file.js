var API_endpoint = "http://127.0.0.1:8080/api/v1/";
var t=1;

$(window).load(function(){
	loadFileData();
});

function loadFileData() {
	console.log('load file data');
	API.send('data', 'get', null, function(res) {
		// Success reponse handle
		res.map(function(item) {
			renderFileItem(item);
		});
	}, function(err){
       // Error handle
	});
}

function renderFileItem(item) {
    var htmlText =''
    if (t==0){htmlText+= '<div class="row">';}
    //them 1 method lay user post
    // thie lap lai time post = timenow - created_at
    htmlText +=''
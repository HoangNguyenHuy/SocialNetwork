var API_endpoint = "http://127.0.0.1:8080/api/v1/";



// clear all the local storage- Logout
$('#clear').click( function() {
localStorage.clear();
console.log(window.localStorage.getItem('token'));
window.location = 'index.html';
return false;
});

$(window).load(function(){
	loadPostData();
});

function loadPostData() {
	console.log('load post data');
	API.send('post', 'get', null, function(res) {
		// Success reponse handle
		res.map(function(item) {
			renderPostItem(item);
		});
	}, function(err){
		// Error handle		
	});
}

function renderPostItem(item) {
	console.log(item);
}


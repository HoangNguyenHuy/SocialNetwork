var API_endpoint = "http://127.0.0.1:8080/api/v1/";



// clear all the local storage- Logout
$('#clear').click( function() {
localStorage.clear();
window.location = 'index.html';
return false;
});



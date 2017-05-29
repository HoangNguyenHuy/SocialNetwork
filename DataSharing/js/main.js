var API_endpoint = "http://127.0.0.1:8000/api/v1/";



// clear all the local storage- Logout
$('#clear').click( function() {
window.localStorage.clear();
location = 'index.html';
return false;
});


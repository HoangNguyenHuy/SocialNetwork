var API_endpoint = "http://127.0.0.1:8080/api/v1/";


$(document).load(function(){
    var x = localStorage.getItem('token');
    if (x !== null) {
        alert("ok");
  } else {
    alert("not login !");
//    window.location = 'index.html';
    // localStorage not defined
}
});

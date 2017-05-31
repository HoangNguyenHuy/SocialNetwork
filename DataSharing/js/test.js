var API_endpoint = "http://127.0.0.1:8080/api/v1/";


$(window).load(function(){
    var x = localStorage.getItem('token');
    console.log(x);
    if (x === null) {
    window.location = 'index.html';
    // localStorage not defined
}
});

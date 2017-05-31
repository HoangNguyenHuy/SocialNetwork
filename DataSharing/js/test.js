var API_endpoint = "http://127.0.0.1:8080/api/v1/";


$(window).load(function(){
  if (typeof localStorage !== 'undefined') {
    var x = localStorage.getItem('mod');
  } else {
    alert("not login !");
    window.location = 'index.html';
    // localStorage not defined
}
});

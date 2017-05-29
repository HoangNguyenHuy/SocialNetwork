function loadAjax(el){
	var MaTin =$(el).attr('data-id');
	$.ajax({
		  url: '/Box/getTin',
		  cache: false,
		  async: false,
		  type: 'POST',
		  data: {'sessionId':MaTin},
		  success: function (result) {
				alert(result);
			  $('#modal-content').html(result);
			  
		  }
	});
}
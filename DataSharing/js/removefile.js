function removeDummy() {
		//$("button").click(function () {
		//$(this).parent().closest('#dummy').hide();
		//});
		var elem = document.getElementById('dummy');
		elem.parentNode.removeChild(elem);
		return false;
	}
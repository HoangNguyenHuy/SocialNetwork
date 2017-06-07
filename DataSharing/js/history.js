$(window).load(function(){
	loadHistory();
});

var htmlText='';

function loadHistory() {
    API.send('download', 'get', null, function(res) {
		// Success reponse handle
		res.map(function(item) {
			renderHistoryItem(item);
			console.log(item);
		});
        $('#page-ner').append(htmlText);
	}, function(err){
       // Error handle
	});
}

function renderHistoryItem(item) {
    htmlText+='<div class="row">'
    +    '<div id="dummy" class="col-md-12">'
    +        '<div class="panel panel-default">'
    +            '<div class="panel-body">'
    +                '<button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="removeHistory('+item._key+');"><span aria-hidden="true">&times;</span></button>'
    +                '<div class="col-md-2">'
    +                    '<img src="image/filedown.png"/>'
    +                '</div>'
    +                '<div class="col-md-10">'
    +                    '<p>'+item.data.name+'</p>'
    +                    '<p>'+jQuery.timeago(item.created_at)+'</p>'
    +                    '<a id="url" class="a-responsive" target="_blank" href="/home/hoangnguyen/workspace/SocialNetwork/src/download/'+item.data.name+'">/home/hoangnguyen/workspace/SocialNetwork/src/download/'+item.data.name+'</a>'
    +                '</div>'
    +            '</div>'
    +        '</div>'
    +    '</div>'
    +'</div>';
}

function removeHistory(_key) {
    console.log(_key);
    API.send('download/'+_key, 'delete', null, function(res) {
		// Success reponse handle
	}, function(err){
       // Error handle
	});
	location.reload(true);
}
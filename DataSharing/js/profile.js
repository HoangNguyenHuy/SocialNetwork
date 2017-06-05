var API_endpoint = "http://127.0.0.1:8080/api/v1/";
var t=1;
var uploadFileFormData = null;

$(window).load(function(){
	loadPostData();
});

function loadPostData() {
	console.log('load post data');
	var form_data = {
	    user_id : JSON.parse(x).user_id,
	}
	API.send('post/get_list_post_of_user', 'post', form_data, function(res) {
		// Success reponse handle
		res.map(function(item) {
			renderPostItem(item);
		});
	}, function(err){
       // Error handle
	});
}

function renderPostItem(item) {
    var htmlText =''

    if (t==0){htmlText+= '<div class="col-md-6">';}
    htmlText +=''
    +'<div class="panel panel-success post panel-shadow">'
    +    '<div class="post-heading">'
    +        '<div class="pull-left image">'
    +            '<img src="image/member.jpg" class="img-circle avatar" alt="user profile image">'
    +        '</div>'
    +        '<div class="pull-left meta">'
    +            '<div class="title h5">'
    +                '<a href="#"><b>'+item.user.username+'</b></a> đã chia sẽ một bài.'
    +            '</div>'
    +            '<h6 class="text-muted time">' +jQuery.timeago(item.created_at)+ '</h6>'
    +        '</div>'
    +    '</div>'
    +    '<div class="panel-description">'
    +        '<p style="margin-left: 20px;">'+item.content+'</p>'
    +    '</div>'
    +    '<div class="icon">'
    +        '<a href="#"><span class="glyphicon glyphicon-heart"></span> Thích</a>'
    +        '<a data-toggle="collapse" data-target="#'+item.id+'"><span class="glyphicon glyphicon-pencil"></span> Bình luận</a>'
    +        '<a href="#"><span class="glyphicon glyphicon-share-alt"></span> Chia sẻ</a>'
    +    '</div>'
    +    '<div class="post-footer">'
    +        '<div class="input-group">'
    +            '<input id="input-'+item.id+'" class="form-control" placeholder="Add a comment" type="text">'
    +            '<span onClick="addComment('+item.id+');" style="cursor:pointer" class="input-group-addon">'
    +                '<a><i class="fa fa-edit"></i></a>'
    +            '</span>'
    +        '</div>'
    +        '<ul id="'+item.id+'" class="collapse" class="comments-list">'
    +             '<ul class="comments-list" id="comment-'+item.id+'">';
                    var form_data = {
                        post_id: item.id,
                    }
                    API.send('comment/get_comment_of_post','post', form_data, function(res) {
                        // Success reponse handle
                        res.map(function(item2) {
                            renderCommentItem(item2);
                        });
                    }, function(err){
                        // Error handle
                    });
    htmlText+=             '</ul>'
    +        '</ul>'
    +    '</div>'
    +'</div>';
    if (t==0){htmlText+='</div>'; t=1}
    $('#page-inner').append(htmlText);
}

function renderCommentItem(item) {
    var htmlCommentText=''
        +'<li class="comment">'
        + '<a class="pull-left" href="#">'
        + '<img class="avatar" src="image/member.jpg" alt="avatar">'
        + '</a>'
        + '<div class="comment-body">'
        + '<div class="comment-heading">'
        + '<h4 class="user">'+item.user.username+'</h4>'
        + '<h5 class="time">' +jQuery.timeago(item.created_at)+ '</h5>'
        + '</div>'
        + '<p>'+item.comment+'</p>'
        + '</div>'
        + '</li>';
    $('#comment-'+item.post_id).append(htmlCommentText);
}

function addComment(id_post) {
    var form_data = {
	    post_id: id_post,
	    comment: document.getElementById('input-'+id_post).value,
	}
	console.log(form_data);
	API.send('comment', 'post', form_data, function(res) {
		// Success reponse handle
	}, function(err){
		// Error handle
	});
}


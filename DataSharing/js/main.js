var t=1;

$(window).load(function(){
	loadPostData();

});

function loadPostData() {
	console.log('load post data');
	API.send('post/get_post_of_friend', 'get', null, function(res) {
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
//    var htmlCommentText=''
//    var form_data = {
//	    post_id: item.id
//	}
//    API.send('comment/get_comment_of_post','post', form_data, function(res) {
//		// Success reponse handle
//        res.map(function(item) {
//			htmlCommentText+='<li class="comment">'
//                            + '<a class="pull-left" href="#">'
//                            + '<img class="avatar" src="image/member.jpg" alt="avatar">'
//                            + '</a>'
//                            + '<div class="comment-body">'
//                            + '<div class="comment-heading">'
//                            + '<h4 class="user">MungPham</h4>'
//                            + '<h5 class="time">3 minutes ago</h5>'
//                            + '</div>'
//                            + '<p>oh, thanks you</p>'
//                            + '</div>'
//                            + '</li>';
//		});
//	}, function(err){
//		// Error handle
//	});


    if (t==0){htmlText+= '<div class="row">';}
    // thie lap lai time post = timenow - created_at
//    getComment(item.id);
    htmlText +=''
    +   '<div class="col-md-6">'
    +        '<div class="panel panel-success post panel-shadow">'
    +            '<div class="post-heading">'
    +                '<div class="pull-left image">'
    +                    '<img src="image/member.jpg" class="img-circle avatar" alt="user profile image">'
    +                '</div>'
    +                '<div class="pull-left meta">'
    +                    '<div class="title h5">'
    +                        '<a href="#"><b>'+item.user.username+'</b></a> đã chia sẽ một bài.'
    +                    '</div>'
    +                    '<h6 class="text-muted time">' +jQuery.timeago(item.created_at)+ '</h6>'
    +                '</div>'
    +            '</div>'
    +            '<div class="panel-description">'
    +                '<p style="margin-left: 20px;">'+item.content+'</p>'
    +            '</div>'
    +            '<div class="icon">'
    +                '<a href="#"><span class="glyphicon glyphicon-heart"></span> Thích</a>'
    +                '<a data-toggle="collapse" data-target="#'+item.id+'"><span class="glyphicon glyphicon-pencil"></span> Bình luận</a>'
    +                '<a href="#"><span class="glyphicon glyphicon-share-alt"></span> Chia sẻ</a>'
    +            '</div>'
    +            '<div class="post-footer">'
    +                '<div class="input-group">'
    +                    '<input class="form-control" placeholder="Add a comment" type="text">'
    +                     '<span class="input-group-addon">'
    +                        '<a href="#"><i class="fa fa-edit"></i></a>'
    +                    '</span>'
    +                '</div>'
    +                '<ul id="'+item.id+'" class="collapse" class="comments-list">'
//    +                    '<li class="comment">'
//    +                        '<a class="pull-left" href="#">'
//    +                            '<img class="avatar" src="image/user_1.jpg" alt="avatar">'
//    +                        '</a>'
//    +                        '<div class="comment-body">'
//    +                            '<div class="comment-heading">'
//    +                                '<h4 class="user">Huy Hoang Nguyen</h4>'
//    +                                 '<h5 class="time">5 minutes ago</h5>'
//    +                            '</div>'
//    +                            '<p>Yes, I like it !</p>'
//    +                        '</div>'
    +                        '<ul class="comments-list">';
    var form_data = {
	    post_id: item.id,
	}
    API.send('comment/get_comment_of_post','post', form_data, function(res) {
		// Success reponse handle
        res.map(function(item) {
//			htmlText+='<li class="comment">'
//                            + '<a class="pull-left" href="#">'
//                            + '<img class="avatar" src="image/member.jpg" alt="avatar">'
//                            + '</a>'
//                            + '<div class="comment-body">'
//                            + '<div class="comment-heading">'
//                            + '<h4 class="user">'+item.id+'</h4>'
//                            + '<h5 class="time">3 minutes ago</h5>'
//                            + '</div>'
//                            + '<p>oh, thanks you</p>'
//                            + '</div>'
//                            + '</li>';
console.log(item);
		});
	}, function(err){
		// Error handle
	});
//    +                            '<li class="comment">'
//    +                                '<a class="pull-left" href="#">'
//    +                                    '<img class="avatar" src="image/member.jpg" alt="avatar">'
//    +                                '</a>'
//    +                                '<div class="comment-body">'
//    +                                    '<div class="comment-heading">'
//    +                                        '<h4 class="user">MungPham</h4>'
//    +                                        '<h5 class="time">3 minutes ago</h5>'
//    +                                    '</div>'
//    +                                    '<p>oh, thanks you</p>'
//    +                                '</div>'
//    +                            '</li>'
    htmlText+=                            '<li class="comment">'
    +                                '<a class="pull-left" href="#">'
    +                                    '<img class="avatar" src="image/user_1.jpg" alt="avatar">'
    +                                '</a>'
    +                                '<div class="comment-body">'
    +                                    '<div class="comment-heading">'
    +                                        '<h4 class="user">Huy Hoang Nguyen</h4>'
    +                                        '<h5 class="time">3 minutes ago</h5>'
    +                                    '</div>'
    +                                    '<p>oh, No problem :)</p>'
    +                                '</div>'
    +                            '</li>'
    +                        '</ul>'
//    +                    '</li>'
    +                '</ul>'
    +            '</div>'
    +        '</div>'
    +    '</div>';
    if (t==0){htmlText+='</div>'; t=1}
    $('#page').append(htmlText);
}

//function getComment(post){
//
//    var form_data = {
//	    post_id: post
//	}
//    API.send('comment/get_comment_of_post','post', form_data, function(res) {
//		// Success reponse handle
////		console.log(res);
//	}, function(err){
//		// Error handle
//	});
//}
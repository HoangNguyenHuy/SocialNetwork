var API_endpoint = "http://127.0.0.1:8080/api/v1/";
var t=1;
//Dropzone.autoDiscover = false;
var uploadFileFormData = null;

// clear all the local storage- Logout
$('#clear').click( function() {
localStorage.clear();
console.log(window.localStorage.getItem('token'));
window.location = 'index.html';
return false;
});

function load_page() {
    window.location.assign(window.location.href);
}

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
//
//function initDropzone() {
//    var myDropzone = new Dropzone("#upload-dropzone");
//    uploadFileFormData = new FormData("#upload-dropzone");
//    myDropzone.on("addedfile", function(file) {
//
//        uploadFileFormData.append('file', file);
//    });
//}


$('#target').submit(function(e) {
	e.preventDefault();
	var form_data = $(this).serialize();

	API.send('post','post', form_data, function(res) {
		// Success reponse handle
//		console.log(res);
	}, function(err){
		// Error handle
	});
});


$('#targets').submit(function(e) {
	e.preventDefault();
	var form_data = new FormData(this);
	form_data.append('file', $(this).find("[id='targets_file_input']").val());

    console.log(form_data);

	API.send('data','post', form_data, function(res) {
		// Success reponse handle
		console.log(res);
	}, function(err){
		// Error handle
	});
});
//$("#myModals").on('show.bs.modal',function() {
//    console.log('show modal');
//})
$("#targets_file_input").on('change', function(e) {

    handlePreviewUpload(this.files);
});

function handlePreviewUpload(files) {
    console.log(files);
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var imageType = /^image\//;

        if (!imageType.test(file.type)) {
          continue;
        }

        var img = document.createElement("img");
        img.classList.add("preview-img");
        img.file = file;
        $("#upload_preview").append(img); // Assuming that "preview" is the div output where the content will be displayed.

        var reader = new FileReader();
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
        reader.readAsDataURL(file);
  }
}


function renderPostItem(item) {
    var htmlText =''
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
    +                    '<h6 class="text-muted time">' + item.created_at + '</h6>'
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
    +                    '<li class="comment">'
    +                        '<a class="pull-left" href="#">'
    +                            '<img class="avatar" src="image/user_1.jpg" alt="avatar">'
    +                        '</a>'
    +                        '<div class="comment-body">'
    +                            '<div class="comment-heading">'
    +                                '<h4 class="user">Huy Hoang Nguyen</h4>'
    +                                 '<h5 class="time">5 minutes ago</h5>'
    +                            '</div>'
    +                            '<p>Yes, I like it !</p>'
    +                        '</div>'
    +                        '<ul class="comments-list">'
    +                            '<li class="comment">'
    +                                '<a class="pull-left" href="#">'
    +                                    '<img class="avatar" src="image/member.jpg" alt="avatar">'
    +                                '</a>'
    +                                '<div class="comment-body">'
    +                                    '<div class="comment-heading">'
    +                                        '<h4 class="user">MungPham</h4>'
    +                                        '<h5 class="time">3 minutes ago</h5>'
    +                                    '</div>'
    +                                    '<p>oh, thanks you</p>'
    +                                '</div>'
    +                            '</li>'
    +                            '<li class="comment">'
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
    +                    '</li>'
    +                '</ul>'
    +            '</div>'
    +        '</div>'
    +    '</div>';
    if (t==0){htmlText+='</div>'; t=1}
    $('#page').append(htmlText);
}

function getComment(post_id){
data= 'post_id:'+post_id;
    API.send('comment/get_comment_of_post','post', data, function(res) {
		// Success reponse handle
//		console.log(res);
	}, function(err){
		// Error handle
	});
}
var API_endpoint = "http://127.0.0.1:8080/api/v1/";
var t=1;
var htmlText ='<thead>'
        +   '<tr>'
        +      '<th>STT</th>'
        +      '<th>Tên File</th>'
        +      '<th>Ngày upload</th>'
        +      '<th>Kích thước</th>'
        +      '<th>Tải xuống</th>'
        +      '<th>Xóa</th>'
        +      '<th>Chia sẻ</th>'
        +    '</tr>'
        +'</thead>'
        +'<tbody>';


$(window).load(function(){
	loadFileData();
});

function loadFileData() {
	console.log('load file data');
	API.send('data', 'get', null, function(res) {
		// Success reponse handle
		res.map(function(item) {
			renderFileItem(item);
		});
		htmlText+='</tbody>';
		$('#file_table').append(htmlText);
	}, function(err){
       // Error handle
	});
}

function renderFileItem(item) {
    var size = item.capacity;
    var dv = 0;
    var str_dv = 'B';

    while(size >1024){
        size = size/1024;
        dv +=1;
    }
    if (dv==1){str_dv = 'KB';}
    if (dv==2){str_dv = 'MB';}
    if (dv==3){str_dv = 'GB';}

    var n = parseFloat(size);
    x = Math.round(n * 100)/100;
    htmlText +=''
        +   '<tr>'
        +        '<td>'+t+'</td>'
        +        '<td>'+item.name+'</td>'
        +        '<td>'+item.created_at+'</td>'
        +        '<td>'+x+ ' '+str_dv+'</td>'
        +        '<td><a href="#" onClick="downloadFile('+ item.id+')">Tải</a></td>'
        +        '<td><a href="#">Xóa</a></td>'
        +        '<td><a href="#">Chia sẻ</a></td>'
        +    '</tr>';
    t+=1;
}

function downloadFile(id) {
    console.log('download file', id);
    var data = new FormData();

    var form_data = {
        data_id: id
    };
    API.send('data/download', 'post', form_data, function(res) {
		// Success reponse handle
		console.log(res);
//		download(res,"dm.jpg","jpg" );
		download(res, this.files[0].name, this.files[0].type);
	}, function(err){
       // Error handle
	});
}

function getUrl(){
//method nay dung de goi url khi user click vao 1 link
}

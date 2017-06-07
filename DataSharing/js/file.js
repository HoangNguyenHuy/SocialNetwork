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

$.date = function(dateObject) {
        var d = new Date(dateObject);
        var day = d.getDate();
        var month = d.getMonth() + 1;
        var year = d.getFullYear();
        if (day < 10) {
            day = "0" + day;
        }
        if (month < 10) {
            month = "0" + month;
        }
        var date = day + "/" + month + "/" + year;

        return date;
    };


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
        +        '<td>'+$.date(item.created_at)+'</td>'
        +        '<td>'+x+ ' '+str_dv+'</td>'
        +        '<td><a style="cursor:pointer" onClick="downloadFile('+ item.id+')">Tải</a></td>'
        +        '<td><a style="cursor:pointer" onClick="deleteFile('+ item.id+')">Xóa</a></td>'
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
    API.send('download', 'post', form_data, function(res) {
		// Success reponse handle
		console.log(res);
		var pagedown = window.open(res);
        pagedown.location;
//		window.open(res);
//		download(res,"dm.jpg","jpg" );
		download(res, this.files[0].name, this.files[0].type);
	}, function(err){
       // Error handle
	});
}

function deleteFile(id) {
    var form_data = {
        data_id: id
    };
    API.send('data', 'delete', form_data, function(res) {
		// Success reponse handle
	}, function(err){
       // Error handle
	});
	location.reload(true);
}
function main (argv) { 
	//var databaseName = "";
	//var graphName = "";
	//var username = "";
	//var passwd = "";	
	
	var databaseName = "";
	var graphName = "";
	var username = "";
	var passwd = "";	

	for(var i=0; i< argv.length; i++){
		switch(i) {
			case 0:
				databaseName = argv[i];
				break;
			case 1:
				graphName = argv[i];
				break;
			case 2:
				username = argv[i];
				break;
			case 3:
				passwd = argv[i];
				break;
	  	}
	}
	
	var isCreated = false;

	// VERTEX COLLECTION
	var userCollectionName = "sn_users";
	var postCollectionName = "sn_posts";
	var contentCommentCollectionName = "sn_content_comment";
	var dataCollectionName = "sn_datas";
	var groupCollectionName = "sn_groups";
	var activitiesCollectionName = "sn_activities";
	var userNotificationStatusCollectionName = "sn_user_notification";
	var dataNotificationStatusCollectionName = "sn_data_notification";

	// EDGE COLLECTION
	var friendCollectionName = "sn_friend";
	//var postTagCollectionName = "sn_post_tag"; thay the = type trong user_post type se co 3 loai comment, post, tag
	var userPostCollectionName = "sn_user_post";
	var postUserCollectionName = "sn_post_user"; //tag
	var postCommentCollectionName = "sn_post_comment"; 
	var userDataCollectionName = "sn_user_data";
	var userDownloadCollectionName = "sn_user_download";
	var postDataCollectionName = "sn_post_data";
	var userGroupCollectionName = "sn_user_group";
	
	var vertexCollection = [userCollectionName, postCollectionName, contentCommentCollectionName,
						   	dataCollectionName, groupCollectionName, activitiesCollectionName, 
							userNotificationStatusCollectionName, dataNotificationStatusCollectionName,
						   ]

	var edgeCollection = [{'name': friendCollectionName, 'from': userCollectionName, 'to': userCollectionName},
						 {'name': userPostCollectionName, 'from': userCollectionName, 'to': postCollectionName},
						 {'name': userDataCollectionName, 'from': userCollectionName, 'to': dataCollectionName},
						 {'name': postDataCollectionName, 'from': postCollectionName, 'to': dataCollectionName},
						 {'name': userGroupCollectionName, 'from': postCollectionName, 'to': groupCollectionName},
						 {'name': postCommentCollectionName, 'from': postCollectionName, 'to': contentCommentCollectionName},
						 {'name': postUserCollectionName, 'from': postCollectionName, 'to': userCollectionName},
						 {'name': userDownloadCollectionName, 'from': userCollectionName, 'to': dataCollectionName},
						 ]

	//var redundantVertexCollection = []

	//var redundantEdgeCollection = []

	try {
		db._useDatabase(databaseName);
		isCreated = true;
	}
	catch(err) {
		isCreated = false;
	}

	if(!isCreated){
		db._createDatabase(databaseName, [], [{username: username, passwd: passwd, active: true}]);
		db._useDatabase(databaseName);
	}

	var graph_module =  require("org/arangodb/general-graph");
	var graph = isCreated ? graph_module._graph(graphName): graph_module._create(graphName);

	// Add new vertexCollection
	for(var i=0; i<vertexCollection.length; i++){
		var collection = db._collection(vertexCollection[i]);
		if(collection == null)
			graph._addVertexCollection(vertexCollection[i]);
	}

	// Add new edgeCollection
	for(var i=0; i<edgeCollection.length; i++){
		var collection = db._collection(edgeCollection[i].name);
		if(collection == null)
			graph._extendEdgeDefinitions(graph_module._relation(edgeCollection[i].name, [edgeCollection[i].from], [edgeCollection[i].to]));
	}

	/*// Delete redundant edgeCollection
	for(var i=0; i<redundantEdgeCollection.length; i++){
		var collection = db._collection(redundantEdgeCollection[i]);
		if(collection !== null){
			try{
				graph._deleteEdgeDefinition(redundantEdgeCollection[i]);
			}catch(err){
				console.log(err)
			}

			db._drop(redundantEdgeCollection[i]);
		}
	}

	// Delete redundant vertexCollection
	for(var i=0; i<redundantVertexCollection.length; i++){
		var collection = db._collection(redundantVertexCollection[i]);
		if(collection !== null){
			try{
				graph._removeVertexCollection(redundantVertexCollection[i]);
			}catch(err){
				console.log(err)
			}

			db._drop(redundantVertexCollection[i]);
		}
	}*/
}

main(ARGUMENTS);
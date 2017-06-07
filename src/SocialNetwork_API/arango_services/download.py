from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.arango_services import ArangoBaseService
from SocialNetwork_API.const import ArangoVertex, ArangoEdge


class ArangoDownloadService(ArangoBaseService):

    @classmethod
    def save_download(cls, data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoEdge.USER_DOWNLOAD,ArangoVertex.DOWNLOAD,ArangoEdge.DOWNLOAD_DATA]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Add post to graph vertex
                ArangoCore.add_vertex_to_collection(ArangoVertex.DOWNLOAD, data, transaction)
                # Add user_download to graph edge
                ArangoCore.add_user_download_to_collection(ArangoEdge.USER_DOWNLOAD, ArangoVertex.USER, data['user_id'],
                                                  ArangoVertex.DOWNLOAD, data['id'], transaction)
                ArangoCore.add_edge_to_collection(ArangoEdge.DOWNLOAD_DATA, ArangoVertex.DOWNLOAD, data['id'],
                                                           ArangoVertex.DATA, data['data_id'], transaction)
                transaction.commit()
            return True
        except Exception as exception:
            raise exception

    @classmethod
    def delete_download_history(cls, data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoEdge.USER_DOWNLOAD]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                ArangoCore.delete_edge_from_collection(ArangoEdge.USER_DOWNLOAD, data.get('_key'), transaction)
                transaction.commit()

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def get_download_history(cls, download_id):
        try:
            query_string = "LET downloads =(FOR download IN sn_user_download FILTER download._key==@download_id LIMIT 1 RETURN download) RETURN downloads[0]"
            parameter = {'download_id': download_id}
            result = ArangoCore.execute_query(query_string, parameter)
            return result[0] if len(result) > 0 else None
        except Exception as exception:
            raise exception

    @classmethod
    def get_download_history_of_user(cls, user_id):
        try:
            user_id = 'sn_users/'+user_id
            query_string = "LET historys = (FOR v,history IN OUTBOUND @user_id sn_user_download " \
                           "SORT history.created_at DESC " \
                           "RETURN merge(history,{infor:v})) " \
                           "FOR history IN historys " \
                           "FOR data IN sn_datas " \
                           "FILTER data.id == history.infor.data_id " \
                           "RETURN merge(history,{data:data}) "
            parameter = {'user_id': user_id}
            return ArangoCore.execute_query(query_string, parameter)
        except Exception as exception:
            raise exception

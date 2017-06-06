from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.arango_services import ArangoBaseService
from SocialNetwork_API.const import ArangoVertex, ArangoEdge


class ArangoDownloadService(ArangoBaseService):

    @classmethod
    def save_download(cls, data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoEdge.USER_DOWNLOAD]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Add user_download to graph edge
                ArangoCore.add_user_download_to_collection(ArangoEdge.USER_DOWNLOAD, ArangoVertex.USER, data['user_id'],
                                                  ArangoVertex.DATA, data['data_id'], data['id'], transaction)
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
            query_string = "FOR v,download IN OUTBOUND @user_id sn_user_download " \
                           "SORT download.created_at DESC " \
                           "RETURN merge(download,{data:v})"
            parameter = {'user_id': user_id}
            return ArangoCore.execute_query(query_string, parameter)
        except Exception as exception:
            raise exception

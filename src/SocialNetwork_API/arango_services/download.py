from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.arango_services import ArangoBaseService
from SocialNetwork_API.const import ArangoVertex, ArangoEdge


class ArangoDownloadService(ArangoBaseService):
    @classmethod
    def save_download(cls, data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoEdge.USER_DATA]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Add user_post to graph edge
                ArangoCore.add_edge_to_collection(ArangoEdge.USER_DATA, ArangoVertex.USER, data['user_id'],
                                                  ArangoVertex.DATA, data['id'], transaction)
                transaction.commit()
            return True
        except Exception as exception:
            raise exception

    def delete_data(cls, data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoVertex.DATA, ArangoEdge.USER_DATA]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                data_id = data.get('id')
                user_id = data.get('user_id')
                ArangoCore.delete_vertex_from_collection(ArangoVertex.DATA, data_id, transaction)
                key = '{0}-{1}'.format(user_id, data_id)
                ArangoCore.delete_edge_from_collection(ArangoEdge.USER_DATA, key, transaction)
                transaction.commit()

            return True
        except Exception as exception:
            raise exception

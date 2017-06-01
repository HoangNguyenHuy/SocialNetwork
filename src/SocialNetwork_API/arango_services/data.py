from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.arango_services import ArangoBaseService
from SocialNetwork_API.const import ArangoVertex, ArangoEdge


class ArangoDataService(ArangoBaseService):
    @classmethod
    def save_post(cls, file_data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoVertex.DATA] + [ArangoEdge.USER_DATA]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Add post to graph vertex
                ArangoCore.add_vertex_to_collection(ArangoVertex.DATA, file_data, transaction)
                # Add user_post to graph edge
                ArangoCore.add_edge_to_collection(ArangoEdge.USER_DATA, ArangoVertex.USER, file_data['user_id'],
                                                  ArangoVertex.DATA, file_data['id'], transaction)
                transaction.commit()
            return True
        except Exception as exception:
            raise exception
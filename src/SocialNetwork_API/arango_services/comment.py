from SocialNetwork_API.arango_services.base import ArangoBaseService
from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.const import ArangoVertex, ArangoEdge

class ArangoCommentService(ArangoBaseService):
    @classmethod
    def save_comment(cls, comment_data):
        try:
            database = ArangoCore.get_database()
            collections = [ArangoVertex.COMMENT] + [ArangoEdge.POST_COMMENT] + [ArangoVertex.ACTIVITY]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Add post to graph vertex
                ArangoCore.add_vertex_to_collection(ArangoVertex.COMMENT, comment_data, transaction)
                # Add user_post to graph edge
                ArangoCore.add_edge_to_collection(ArangoEdge.POST_COMMENT, ArangoVertex.POST, comment_data['post_id'],
                                                      ArangoVertex.COMMENT, comment_data['id'], transaction)
                transaction.commit()
            return True
        except Exception as exception:
            raise exception
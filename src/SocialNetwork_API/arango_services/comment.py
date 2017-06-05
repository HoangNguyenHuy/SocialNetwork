from SocialNetwork_API.arango_services import ArangoBaseService
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

    @classmethod
    def get_commnet(cls, post_id):
        post_id = 'sn_posts/' + str(post_id)
        query_string = "FOR comment IN OUTBOUND @post_id sn_post_comment OPTIONS {bfs: true, uniqueVertices: 'global'} " \
                       "SORT comment.created_at ASC " \
                       "LET user = (FOR user IN sn_users FILTER user._key == TO_STRING(comment.user_id) LIMIT 1  " \
                       "RETURN user)[0] " \
                       "RETURN merge(comment,{user})"
        parameter = {'post_id': post_id}
        result = ArangoCore.execute_query(query_string, parameter)
        return result
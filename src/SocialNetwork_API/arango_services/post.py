from SocialNetwork_API.arango_services.base import ArangoBaseService
from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.const import ArangoVertex, ArangoEdge, POST_COLLECTIONS

class ArangoPostService(ArangoBaseService):
    @classmethod
    def save_post(cls, post_data):
        try:
            database = ArangoCore.get_database()
            collections = POST_COLLECTIONS
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Add post to graph vertex
                ArangoCore.add_vertex_to_collection(ArangoVertex.POST, post_data, transaction)
                # Add user_post to graph edge
                ArangoCore.add_edge_to_collection(ArangoEdge.USER_POST, ArangoVertex.USER, post_data['user_id'],
                                                      ArangoVertex.POST, post_data['id'], transaction)
                transaction.commit()
            return True
        except Exception as exception:
            raise exception

    @classmethod
    def get_post_of_friend(cls, user_id):
        user_id = 'sn_users/' + str(user_id)
        query_string = "LET friends = (" \
                       "FOR user IN OUTBOUND @user_id sn_friend OPTIONS {bfs: true, uniqueVertices: 'global'} " \
                       "return user._id) " \
                       "let post=(" \
                       "for friend in friends for post in outbound friend sn_user_post return post) " \
                       "return post "
        parameter = {'user_id': user_id}
        result = ArangoCore.execute_query(query_string, parameter)

        return result
from SocialNetwork_API.arango_services import ArangoBaseService
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
        #query with graph
        # FOR post IN 1..2 OUTBOUND @user_id sn_friend, sn_user_post
        # câu query này sẽ select theo 2 cạnh của sn_friend và sn_user_post với giá trị user_id và select hết tất cả các item select đc gồm cả user và post
        # để chỉ lấy được các post thì t phải filter ra các item có user_type == null vì post ko có user_type chỉ user mới có user_type
        query_string = "FOR post IN 1..2 OUTBOUND @user_id sn_friend, sn_user_post OPTIONS {bfs: true, uniqueVertices: 'global'} " \
                       "FILTER post.user_type == NULL " \
                       "SORT post.created_at DESC " \
                       "LET user = (FOR user IN sn_users FILTER user._key == TO_STRING(post.user_id) LIMIT 1 " \
                       "RETURN user)[0] " \
                       "RETURN merge(post,{user})"
        #query with vertex and edge
        # query_string = "LET friends = (" \
        #                "FOR user IN OUTBOUND @user_id sn_friend OPTIONS {bfs: true, uniqueVertices: 'global'} " \
        #                "RETURN user._id) " \
        #                "LET post=(" \
        #                "FOR friend IN friends " \
        #                "FOR post IN OUTBOUND friend sn_user_post OPTIONS {bfs: true, uniqueVertices: 'global'}" \
        #                "SORT post.created_at DESC " \
        #                "RETURN post) " \
        #                "RETURN post "
        parameter = {'user_id': user_id}
        result = ArangoCore.execute_query(query_string, parameter)

        return result

    @classmethod
    def get_post_of_user(cls, user_id):
        user_id = 'sn_users/' + str(user_id)
        query_string = "FOR post IN OUTBOUND @user_id sn_user_post OPTIONS {bfs: true, uniqueVertices: 'global'} " \
                       "SORT post.created_at DESC " \
                       "LET user = (FOR user IN sn_users FILTER user._key == TO_STRING(post.user_id) LIMIT 1 " \
                       "RETURN user)[0] " \
                       "RETURN merge(post,{user})"
        parameter = {'user_id': user_id}
        result = ArangoCore.execute_query(query_string, parameter)
        return result


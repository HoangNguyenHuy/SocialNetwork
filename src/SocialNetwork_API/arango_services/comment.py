# from SocialNetwork_API.arango_services.base import ArangoBaseService
# from SocialNetwork_API.arango_core import ArangoCore
# from SocialNetwork_API.const import ArangoVertex, ArangoEdge
#
# class ArangoCommentService(ArangoBaseService):
#     @classmethod
#     def save_comment(cls, post_data):
#         try:
#             database = ArangoCore.get_database()
#             collections = [ArangoVertex.COMMENT] + [ArangoEdge] + [ArangoVertex.ACTIVITY]
#             with database.transaction(write=collections, commit_on_error=False) as transaction:
#                 # Add post to graph vertex
#                 ArangoCore.add_vertex_to_collection(ArangoVertex.POST, post_data, transaction)
#                 # Add user_post to graph edge
#                 ArangoCore.add_edge_to_collection(ArangoEdge.USER_POST, ArangoVertex.USER, post_data['user_id'],
#                                                       ArangoVertex.POST, post_data['id'], transaction)
#                 transaction.commit()
#             return True
#         except Exception as exception:
#             raise exception
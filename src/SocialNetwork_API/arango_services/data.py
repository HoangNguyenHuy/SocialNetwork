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

    @classmethod
    def get_data(cls, data_id, get_name=False):
        try:
            if get_name:
                query_string = "FOR data IN sn_datas FILTER data.id == @data_id LIMIT 1 RETURN data.name"
            else:
                query_string = "FOR data IN sn_datas FILTER data.id == @data_id LIMIT 1 RETURN data"
            parameter = {'data_id': data_id}
            result = ArangoCore.execute_query(query_string, parameter)
            return result[0] if len(result) > 0 else None
        except Exception as exception:
            raise exception

    @classmethod
    def get_data_of_user(cls, user_id):
        user_id = 'sn_users/' + str(user_id)
        query_string = "FOR data IN OUTBOUND @user_id sn_user_data OPTIONS {bfs: true, uniqueVertices: 'global'} " \
                       "SORT data.created_at DESC " \
                       "RETURN data"
        parameter = {'user_id': user_id}
        result = ArangoCore.execute_query(query_string, parameter)
        return result

    @classmethod
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
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
            query_string = "FOR data IN sn_datas FILTER data.id == @data_id LIMIT 1 RETURN data"
            if get_name:
                query_string = "FOR data IN sn_datas FILTER data.id == @data_id LIMIT 1 RETURN data.name"
            parameter = {'data_id': data_id}
            result = ArangoCore.execute_query(query_string, parameter)
            return result[0] if len(result) > 0 else None
        except Exception as exception:
            raise exception

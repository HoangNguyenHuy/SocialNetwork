from SocialNetwork_API.arango_services.base import ArangoBaseService
from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.const import ArangoVertex, ArangoEdge, USER_FIELDS


class ArangoUserService(ArangoBaseService):
    @classmethod
    def get_user_channels_by_user_id(cls, user_id):
        try:
            start_id = 'rv_users/{0}'.format(user_id)
            query_string = "FOR v, e IN OUTBOUND @start_id rv_user_channels OPTIONS {bfs: true, uniqueVertices: 'global'} RETURN e.name "

            parameter = {'start_id': str(start_id)}

            return ArangoCore.execute_query(query_string, parameter)
        except Exception as exception:
            raise exception

    @classmethod
    def get_user_channels_by_band_id(cls, band_id):
        try:
            start_id = 'rv_users/{0}'.format(band_id)
            query_string = "FOR user IN INBOUND @start_id rv_user_follows OPTIONS {bfs: true, uniqueVertices: 'global'} "
            query_string += "LET channels = (FOR v, e IN OUTBOUND user._id rv_user_channels OPTIONS {bfs: true, uniqueVertices: 'global'} RETURN e.name) "
            query_string += "RETURN {'user_id': user.id, 'channels': channels}"

            parameter = {'start_id': str(start_id)}

            channels = []
            user_channels = ArangoCore.execute_query(query_string, parameter)
            for user_channel in user_channels:
                channels += user_channel['channels']

            return channels
        except Exception as exception:
            raise exception

    @classmethod
    def del_user_channel(cls, channel):
        try:
            channel_id = '{0}/{1}'.format('rv_channels', channel)
            database = ArangoCore.get_database()
            collections = [ArangoEdge.USER_CHANNEL]

            with database.transaction(write=collections, commit_on_error=False) as transaction:
                command = '''
                   function () {{
                       // Get database
                       var db = require("internal").db;

                       // Delete all edges relate to content_id
                       db._query("For edge IN rv_user_channels FILTER edge._to == '{0}' REMOVE {{_key: edge._key}} IN rv_user_channels");

                       return true;
                   }}'''.format(channel_id)

                transaction.execute(command)

                transaction.commit()
            return True
        except Exception as exception:
            raise exception

    @classmethod
    def create_edge_collection(cls, user_id):
        try:
            graph = ArangoCore.get_graph()

            # Create a new edge definition (and a new edge collection)
            collection_name = '{0}_{1}'.format(ArangoEdge.USER_POST, user_id)
            graph.create_edge_definition(
                name=collection_name,
                from_collections=[ArangoVertex.USER],
                to_collections=[ArangoVertex.POST]
            )
        except Exception as exception:
            raise exception

    @classmethod
    def update_user_posts(cls, user_id, band_id):
        try:
            post_ids = ArangoPostService.get_post_ids_by_band_id(band_id)
            edge_collection_name = '{0}_{1}'.format(ArangoEdge.USER_POST, user_id)
            batch = ArangoCore.get_batch()

            for post_id in post_ids:
                batch.collection(edge_collection_name).insert({'_key': '{0}-{1}'.format(user_id, post_id),
                                                               '_from': '{0}/{1}'.format(ArangoVertex.USER, user_id),
                                                               '_to': '{0}/{1}'.format(ArangoVertex.POST, post_id)})

            batch.commit()
        except Exception as exception:
            raise exception

    @classmethod
    def add_user_channel(cls, user_id, channel):
        try:
            ArangoCore.add_channel_to_collection(ArangoEdge.USER_CHANNEL, ArangoVertex.USER, user_id,
                                              ArangoVertex.CHANNEL, channel)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def save_user(cls, user_id, user_data=None, is_new=True):
        try:
            user_data = cls.prepare_data_to_save(user_id, user_data, is_new)
            database = ArangoCore.get_database()
            collections = [ArangoVertex.USER]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                if is_new:
                    ArangoCore.add_vertex_to_collection(ArangoVertex.USER, user_data, transaction)
                else:
                    ArangoCore.update_vertex_in_collection(ArangoVertex.USER, user_data, transaction)
                    user_data['_id'] = '{0}/{1}'.format('rv_users', user_data['id'])

                transaction.commit()
            return True
        except Exception as exception:
            raise exception

    @classmethod
    def prepare_data_to_save(cls, user_id, user_data, is_new=True):
        data_to_save = {} if is_new else ArangoCore.get_vertex_in_collection(ArangoVertex.USER, user_id)
        for user_field in USER_FIELDS:
            if user_data and user_field in user_data:
                data_to_save[user_field] = user_data[user_field]

        # if data_to_save['avatar'] != '' and data_to_save['avatar'][:4] != 'http':
        #     data_to_save['avatar_host'] = settings.AWS_URL if data_to_save['is_avatar_uploaded_to_s3'] else settings.API_URL
        # else:
        #     data_to_save['avatar_host'] = ''
        #
        # if data_to_save['background'] != '':
        #     data_to_save['background_host'] = settings.AWS_URL if data_to_save['is_background_uploaded_to_s3'] else settings.API_URL
        # else:
        #     data_to_save['background_host'] = ''

        return data_to_save

    @classmethod
    def update_band(cls, user_id, follow_count, transaction):
        band_data = ArangoCore.get_vertex_in_collection(ArangoVertex.BAND, user_id)
        band_data['follow_count'] = follow_count

        ArangoCore.update_vertex_in_collection(ArangoVertex.BAND, band_data, transaction)
        band_data['_id'] = '{0}/{1}'.format('rv_users', user_id)
        ArangoCore.update_vertex_in_collection(ArangoVertex.USER, band_data, transaction)

    @classmethod
    def add_friend(cls, user_friend_data, activity_data):
        if '_user_cache' in user_friend_data:
            del user_friend_data['_user_cache']
        try:
            database = ArangoCore.get_database()
            collections = ArangoEdge.FRIEND
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                ArangoCore.add_edge_to_collection(ArangoEdge.FRIEND, ArangoVertex.USER,
                                                  user_friend_data['user_id'],
                                                  ArangoVertex.USER, user_friend_data['friend_user_id'], transaction)
                transaction.commit()

        except Exception as exception:
            raise exception

    @classmethod
    def unfollow_band(cls, user_id, band_data):
        try:
            database = ArangoCore.get_database()
            collections = ACTIVITY_COLLECTIONS
            collections += [ArangoVertex.BAND, ArangoEdge.USER_FOLLOW]
            with database.transaction(write=collections, commit_on_error=False) as transaction:
                # Remove relation between 2 user
                _key = '{0}-{1}'.format(user_id, band_data['user_id'])
                ArangoCore.delete_edge_from_collection(ArangoEdge.USER_FOLLOW, _key)

                # Update band data
                cls.update_band(band_data['user_id'], band_data['follow_count'], transaction)

            transaction.commit()

        except Exception as exception:
            raise exception

    # return user_data

from django.utils import timezone
from arango import ArangoClient
from datetime import date, datetime, timedelta
from django.conf import settings

from SocialNetwork_API.const import ActionType, CollectionType


class ArangoCore(object):
    @classmethod
    def clean_data(cls, data):
        if 'tip_amount' in data:
            data['tip_amount'] = float(data['tip_amount'])

        if '_state' in data:
            del data['_state']

        if '_binding_group_names' in data:
            del data['_binding_group_names']

        for key in data:
            if isinstance(data[key], date) or isinstance(data[key], datetime):
                data[key] = data[key].isoformat()

        # simplejson.dumps(data['tip_amount'], use_decimal=True)
        return data

    @classmethod
    def get_client(cls):
        try:
            return ArangoClient(
                    protocol='http',
                    host=settings.ARANGODB_HOST,
                    port=settings.ARANGODB_PORT,
                    username='root',
                    password=settings.ARANGODB_ROOT_PASS,
                    enable_logging=True
                )
        except Exception as exception:
            raise exception

    @classmethod
    def get_async(cls):
        try:
            database = cls.get_database()
            return database.async(return_result=True)
        except Exception as exception:
            raise exception

    @classmethod
    def get_batch(cls):
        try:
            database = cls.get_database()
            return database.batch(return_result=False)
        except Exception as exception:
            raise exception

    @classmethod
    def get_database(cls):
        try:
            client = cls.get_client()
            arangodb_name = settings.ARANGODB_NAME
            if settings.ARANGODB_IN_TEST_MODE:
                arangodb_name = '{0}{1}'.format(settings.ARANGODB_NAME, settings.ARANGODB_TEST_SUBFIX)
            return client.database(arangodb_name, username=settings.ARANGODB_USER, password=settings.ARANGODB_PASS)
        except Exception as exception:
            raise exception

    @classmethod
    def get_graph(cls):
        try:
            database = cls.get_database()
            arangodb__graph_name = settings.ARANGODB_GRAPH_NAME
            if settings.ARANGODB_IN_TEST_MODE:
                arangodb__graph_name = '{0}{1}'.format(settings.ARANGODB_GRAPH_NAME, settings.ARANGODB_TEST_SUBFIX)
            return database.graph(arangodb__graph_name)
        except Exception as exception:
            raise exception

    # region vertex_collection
    @classmethod
    def get_vertex_collection(cls, collection_name):
        try:
            graph = cls.get_graph()
            return graph.vertex_collection(collection_name)
        except Exception as exception:
            raise exception

    @classmethod
    def get_all_vertex_in_collection(cls, collection_name):
        try:
            collection = cls.get_vertex_collection(collection_name)
            return collection.all()
        except Exception as exception:
            raise exception

    @classmethod
    def get_vertex_in_collection(cls, collection_name, key):
        try:
            collection = cls.get_vertex_collection(collection_name)
            return collection[key]
        except Exception as exception:
            raise exception

    @classmethod
    def has_vertex_in_collection(cls, collection_name, condition):
        try:
            collection = cls.get_vertex_collection(collection_name)
            result = collection.find(condition, 0, 1)
            return len(result._data['result']) > 0
        except Exception as exception:
            raise exception

    @classmethod
    def find_vertex_in_collection(cls, collection_name, condition):
        try:
            collection = cls.get_vertex_collection(collection_name)
            result = collection.find(condition)
            if result:
                return result._data['result']
            else:
                return []
        except Exception as exception:
            raise exception

    @classmethod
    def add_vertex_to_collection(cls, collection_name, data, transaction=None):
        try:
            data['_key'] = str(data['id'])
            data = cls.clean_data(data)

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_vertex_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def update_vertex_in_collection(cls, collection_name, data, transaction=None):
        try:
            data['_key'] = str(data['id'])
            data = cls.clean_data(data)

            if transaction:
                collection = transaction.collection(collection_name)
                collection.update(data)
            else:
                collection = cls.get_vertex_collection(collection_name)
                collection.update(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def delete_vertex_from_collection(cls, collection_name, key, transaction=None):
        try:
            if transaction:
                vertex = transaction.collection(collection_name)[key]
                if vertex:
                    collection = transaction.collection(collection_name)
                    collection.delete(vertex)
            else:
                vertex = cls.get_vertex_in_collection(collection_name, key)
                if vertex:
                    collection = cls.get_vertex_collection(collection_name)
                    collection.delete(vertex)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def delete_vertexes_from_collection(cls, collection_name, vertexes, transaction=None):
        try:
            collection = transaction.collection(collection_name) if transaction else cls.get_vertex_collection(
                collection_name)

            for vertex in vertexes:
                collection.delete(vertex)

            return True
        except Exception as exception:
            raise exception

    # end region vertex_collection

    # region edge_collection
    @classmethod
    def get_edge_collection(cls, collection_name):
        try:
            graph = cls.get_graph()
            return graph.edge_collection(collection_name)
        except Exception as exception:
            raise exception

    @classmethod
    def get_edge_in_collection(cls, collection_name, key):
        try:
            collection = cls.get_edge_collection(collection_name)
            return collection[key]
        except Exception as exception:
            raise exception

    @classmethod
    def find_edge_in_collection(cls, collection_name, condition):
        try:
            collection = cls.get_edge_collection(collection_name)
            result = collection.find(condition)
            if result:
                return result._data['result']
            else:
                return []
        except Exception as exception:
            raise exception

    @classmethod
    def add_edge_to_collection_in_async(cls, collection_name, from_collection_name, from_collection_key, to_collection_name,
                               to_collection_key, async):
        try:
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)
            data = {'_key': _key, '_from': _from, '_to': _to,
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat()}

            async.collection(collection_name).insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_edge_to_collection_in_batch(cls, collection_name, from_collection_name, from_collection_key,
                                        to_collection_name,
                                        to_collection_key, batch):
        try:
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)
            data = {'_key': _key, '_from': _from, '_to': _to}

            batch.collection(collection_name).insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_edge_to_collection(cls, collection_name, from_collection_name, from_collection_key, to_collection_name,
                               to_collection_key, transaction=None):
        try:
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)
            data = {'_key': _key, '_from': _from, '_to': _to,
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat()}

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def update_edge_in_collection(cls, collection_name, data, transaction=None):
        try:
            if transaction:
                collection = transaction.collection(collection_name)
                collection.update(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.update(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def delete_edge_from_collection(cls, collection_name, key, transaction=None):
        try:
            if transaction:
                edge = transaction.collection(collection_name)[key]
                if edge:
                    collection = transaction.collection(collection_name)
                    collection.delete(edge)
            else:
                edge = cls.get_edge_in_collection(collection_name, key)
                if edge:
                    collection = cls.get_edge_collection(collection_name)
                    collection.delete(edge)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def delete_edges_from_collection(cls, collection_name, edges, transaction=None):
        try:
            collection = transaction.collection(collection_name) if transaction else cls.get_edge_collection(
                collection_name)

            for edge in edges:
                collection.delete(edge)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def truncate_collection(cls, collection_name, collection_type=CollectionType.VERTEX):
        # collection_type: 1-Vertex 2-Edge
        try:
            if collection_type == CollectionType.VERTEX:
                collection = cls.get_vertex_collection(collection_name)
            else:
                collection = cls.get_edge_collection(collection_name)

            collection.truncate()

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_activity_edge_to_collection(cls, collection_name, from_collection_name, from_collection_key,
                               to_collection_name, to_collection_key, content_id, transaction=None):
        try:
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)

            data = {'_key': _key, '_from': _from, '_to': _to,
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat(),
                    'content_id': content_id}

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_channel_to_collection(cls, collection_name, from_collection_name, from_collection_key, to_collection_name,
                               to_collection_key, transaction=None):
        try:
            expiration_date = datetime.utcnow().date() + timedelta(days=(7))
            expiration_date = expiration_date.isoformat()
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)
            data = {'_key': _key, '_from': _from, '_to': _to, 'name': to_collection_key,
                    'expiration_date': expiration_date,
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat()}

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_playlist_content_edge_to_collection(cls, collection_name, from_collection_name, from_collection_key,
                                        to_collection_name, to_collection_key, playlist_content_id, display_order, transaction=None):
        try:
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)

            data = {'_key': _key, '_from': _from, '_to': _to,
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat(),
                    'playlist_content_id': playlist_content_id, 'display_order': display_order}

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_interacted_content_to_collection(cls, collection_name, from_collection_name, from_collection_key,
                               to_collection_name, to_collection_key, action_type, transaction=None):
        try:
            _key = '{0}-{1}'.format(from_collection_key, to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)
            liked = action_type == ActionType.LIKE
            commented = action_type == ActionType.COMMENT
            tipped = action_type == ActionType.TIP
            played = action_type == ActionType.PLAY

            data = {'_key': _key, '_from': _from, '_to': _to,
                    'liked_date': str(timezone.now().date()),
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat(),
                    'liked': liked, 'commented': commented, 'tipped': tipped, 'played': played}

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def add_user_download_to_collection(cls, collection_name, from_collection_name, from_collection_key, to_collection_name,
                               to_collection_key, transaction=None):
        try:
            _key = '{0}'.format(to_collection_key)
            _from = '{0}/{1}'.format(from_collection_name, from_collection_key)
            _to = '{0}/{1}'.format(to_collection_name, to_collection_key)
            data = {'_key': _key, '_from': _from, '_to': _to,
                    'created_at': timezone.now().isoformat(), 'updated_at': timezone.now().isoformat()}

            if transaction:
                collection = transaction.collection(collection_name)
                collection.insert(data)
            else:
                collection = cls.get_edge_collection(collection_name)
                collection.insert(data)

            return True
        except Exception as exception:
            raise exception
    # end region edge_collection

    @classmethod
    def execute_query(cls, query_string, parameter):
        database = ArangoCore.get_database()
        result = database.aql.execute(
            query_string,
            bind_vars=parameter
        )
        return result._data['result'] if result else []
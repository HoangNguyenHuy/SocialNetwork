from django.utils import timezone
from SocialNetwork_API.services.base import BaseService
from SocialNetwork_API.arango_core import ArangoCore
from SocialNetwork_API.const import ArangoVertex, ArangoEdge, ActionType


class ArangoBaseService(BaseService):
    @classmethod
    def update_user_interacted_contents(cls, user_id, content_id, action_type, transaction):
        key = '{0}-{1}'.format(user_id, content_id)
        user_content = ArangoCore.get_edge_in_collection(ArangoEdge.USER_INTERACTED_CONTENT, key)
        if not user_content:
            if action_type in [ActionType.LIKE, ActionType.COMMENT, ActionType.TIP, ActionType.PLAY]:
                ArangoCore.add_interacted_content_to_collection(ArangoEdge.USER_INTERACTED_CONTENT, ArangoVertex.USER,
                                                  user_id, ArangoVertex.CONTENT, content_id, action_type, transaction)
        else:
            user_content['updated_at'] = timezone.now().isoformat()
            if action_type == ActionType.LIKE:
                user_content['liked'] = True
                user_content['liked_date'] = str(timezone.now().date())
            elif action_type == ActionType.COMMENT:
                user_content['commented'] = True
            elif action_type == ActionType.TIP:
                user_content['tipped'] = True
            elif action_type == ActionType.PLAY:
                user_content['played'] = True
            elif action_type == ActionType.UNLIKE:
                user_content['liked'] = False
            elif action_type == ActionType.UNCOMMENT:
                user_content['commented'] = False

            ArangoCore.update_edge_in_collection(ArangoEdge.USER_INTERACTED_CONTENT, user_content, transaction)

        return user_content

    @classmethod
    def has_vertex_in_collection(cls, collection_name, condition):
        return ArangoCore.has_vertex_in_collection(collection_name, condition)

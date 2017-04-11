from SocialNetwork_API.services.base import BaseService

class PostService(BaseService):
    def save(cls, user, post_data, instance=None):
        try:
            print("ass")
        except Exception as exception:
            cls.log_exception(exception)
            raise exception
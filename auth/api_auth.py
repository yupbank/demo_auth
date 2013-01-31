from tastypie.authentication import Authentication
from tastypie.authorization import Authorization


class MyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True
        return False



class MyAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        if request.user.id:
            return True
        else:
            return False

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            print object_list.model
            return object_list.filter(id=request.user.id)
        return object_list.none()
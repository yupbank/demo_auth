from tastypie.resources import ModelResource
from .models import MyUser, UserInfo

class MyUserResource(ModelResource):
    class Meta:
        queryset = MyUser.objects.all()
        resource_name = 'user'


class UserInfoResource(ModelResource):
    class Meta:
        queryset = UserInfo.objects.all()
        resource_name = 'info'

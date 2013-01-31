from tastypie.resources import ModelResource
from .models import MyUser, UserInfo
from .api_auth import MyAuthentication, MyAuthorization

from django.db import models
from tastypie.models import create_api_key


#models.signals.post_save.connect(create_api_key, sender=MyUser)

class MyUserResource(ModelResource):
    class Meta:
        queryset = MyUser.objects.all()
        resource_name = 'user'
        authorization = MyAuthorization() #for limits
        authentication = MyAuthentication() #for visits


class UserInfoResource(ModelResource):
    class Meta:
        queryset = UserInfo.objects.all()
        resource_name = 'info'
        authorization = MyAuthorization() #for limits
        authentication = MyAuthentication() #for visits



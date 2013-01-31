from .models import MyUser, UserInfo, Auth
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.contrib import admin

admin.site.register(MyUser)
admin.site.register(UserInfo)
admin.site.register(Auth)
admin.site.unregister(Site)
admin.site.unregister(User)
admin.site.unregister(Group)



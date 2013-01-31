# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import register, UserInfo
from.baseview import BaseView
from django.contrib import auth
import json


def index(request):
    return render_to_response('index.html')

def login_required(func):
    def _(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(self, request, *args, **kwargs)
        else:
            return HttpResponse(content=json.dumps(dict(error='u need to login first')))
    return _

def login_forbidden(func):
    def _(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponse(content=json.dumps(dict(error='u have already logged in')))
        else:
            return func(self, request, *args, **kwargs)
    return _

class Register(BaseView):
    @login_forbidden
    def post(self, request):
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        cell_phone = request.POST.get('cell_phone', None)
        photo = request.POST.get('photo', None)
        password = request.POST.get('password', None)
        user = register(email, name, cell_phone, photo, password)
        if user:
            auth.login(request, user)
            return self.render(data=user.to_dict())
        else:
            return self.render(error="sorry, something wrong! please retry")

    def get(self, request):
        return self.render(error="please use post method")

class Login(BaseView):
    def get(self, request):
        return self.render(error="don't support get method")

    @login_forbidden
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return self.render(data=user.to_dict())
        return self.render(error="something wrong with the input")

class Logout(BaseView):
    @login_required
    def get(self, request):
        return self.render(error="don't support get method")

    @login_required
    def post(self, request):
        auth.logout(request)
        return self.render(message='good bye')


class UserInfoHandler(BaseView):
    @login_required
    def get(self, request):
        user_info = UserInfo.objects.get(user=request.user)
        return self.render(user_info.to_dict())

class Password(BaseView):
    def get(self):
        pass

class ResetPassword(BaseView):
    def get(self):
        pass

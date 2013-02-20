# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import register, UserInfo, Auth, MyUser
from.baseview import BaseView
from django.contrib import auth
from kit import Random
from .state import SET_NEW, SMALL_KV
import json



def index(request):
    return render_to_response('index.html', {'Loggedin':request.user.is_authenticated()})

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

    @login_required
    def post(self, request):
        name = request.POST.get('name', None)
        cell_phone = request.POST.get('cell_phone', None)
        photo = request.POST.get('photo', None)
        user = request.user
        UserInfo.set(user, name, photo, cell_phone)
        return self.render(message='success')


class Password(BaseView):
    def get(self, request):
        return self.render(error="don't support get method")

    @login_required
    def post(self, request):
        new_password = request.POST.get('password', None)
        if new_password:
            Auth.set(request.user, new_password)
            return self.render(data=request.user.to_dict(), message='password successfully updated')
        return self.render(error='somthing went wrong')

class ResetPassword(BaseView):
    def get(self, request):
        new_password = Random(8)
        email = request.GET.get('email')
        SMALL_KV[email] = new_password
        return self.render(new_password=new_password)

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('pass_word', None)
        new_password = SMALL_KV.get(email, None)
        if password and new_password and password == new_password:
            if MyUser.objects.filter(email=email).exists():
                user = MyUser.objects.get(email=email)
                user.state = SET_NEW
                user.save()
                Auth.set(user, password)
                return self.render(message='success')
        return self.render(error='something went wrong')




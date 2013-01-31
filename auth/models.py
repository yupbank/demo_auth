from django.db import models
from hashlib import sha256
import os
from .state import NEW_USER

def hash_password(user_id, password):
    return sha256('%s%s'%(user_id, password)).hexdigest()


class MyUser(models.Model):
    email = models.EmailField(unique=True)
    state = models.IntegerField(default=NEW_USER)

    def is_authenticated(self):
        return True


    class DoesNotExist(Exception):
        pass

    def to_dict(self):
        return dict(
                        id = self.id,
                        email = self.email,
                        state = self.state
                    )

    def __unicode__(self):
        return '<%s>'%self.email
    
    backend = 'auth.auth_backend.MyUserModelBackend'

def get_image_path(instance, filename):
    return os.path.join('static', str(instance.user.id), filename)


class UserInfo(models.Model):
    user = models.ForeignKey(MyUser)
    name = models.CharField(max_length=200)
    photo = models.ImageField(blank=True, upload_to=get_image_path)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return dict(
            id = self.user.id,
            name = self.name,
            photo = self.photo._get_url() if self.photo else None,
            cell_phone = self.cell_phone,
            create_time = str(self.create_time)
        )

    @classmethod
    def get_or_create(cls, user):
        try:
            user_info = cls.objects.get(user=user)
        except Exception, e:
            user_info = cls(user=user)
        return user_info

    @classmethod
    def set(cls, user, name, photo, cell_phone):
        user_info = cls.get_or_create(user=user)
        user_info.name = name
        user_info.photo = photo
        user_info.cell_phone = cell_phone
        user_info.save()

    def __unicode__(self):
        return self.name


class Auth(models.Model):
    user = models.ForeignKey(MyUser)
    token = models.TextField()

    @classmethod
    def get_or_create_by_user(cls, user):
        try:
            user = cls.objects.get(user=user)
        except Exception, e:
            user = cls(user=user)

        return user

    @classmethod
    def set(cls, user, password):
        auth = cls.get_or_create_by_user(user)
        token = hash_password(user.pk, password)
        auth.token = token
        auth.save()

        return auth

    def check_password(self, password):
        token = hash_password(self.user.pk, password)
        if self.token == token:
            return self.user

    def __unicode__(self):
        return str(self.user)

def email_in_use(email):
    if MyUser.objects.filter(email=email).exists():
        return True

def register(email, name, photo, cell_phone, passwd):
    if not email_in_use(email):
        user = MyUser(email=email)
        user.save()

        user_info = UserInfo.get_or_create(user=user)
        user_info.name = name
        user_info.photo = photo
        user_info.cell_phone = cell_phone
        user_info.save()

        Auth.set(user, passwd)

        return user


def login(email, password):
    try:
        user = MyUser.objects.get(email=email)
    except Exception,e:
        return 'valid email', None

    try:
        auth = Auth.objects.get(user=user)
    except Exception, e:
        return 'valid password', None

    user = auth.check_password(password)
    if not user:
        return 'valid password', None

    return user, True












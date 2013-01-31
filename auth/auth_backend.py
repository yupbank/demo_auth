from django.contrib.auth.backends import ModelBackend
from .models import MyUser




class MyUserModelBackend(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = self.user_class.objects.get(email=email)
            if user.auth_set.get().check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        return MyUser


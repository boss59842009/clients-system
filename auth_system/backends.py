from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumberBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = kwargs.get("phone_number") or username

        if phone is None or password is None:
            return None

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
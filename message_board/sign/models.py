from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import User
from project.models import User
from django import forms


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, k=5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user

class BaseRegisterForm(SignupForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    def save(self, request):
        user = super(BaseRegisterForm, self).save(request)
        User.objects.create()
        return user
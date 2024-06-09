import requests
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from project.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user',

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, template_name='account/invalid_code.html' )

        return redirect('account_login')


class ProfileViev(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/main.html'
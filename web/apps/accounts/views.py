from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
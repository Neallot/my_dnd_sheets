from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm


class RegisterView(CreateView):
    """Регистрация нового пользователя с автоматическим входом после успеха."""

    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('character-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

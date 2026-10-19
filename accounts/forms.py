from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации: логин, пароль и выбор роли (игрок/мастер)."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    # Додаткові поля для форми реєстрації (необов'язково)
    # наприклад, номер телефону, дата народження тощо

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)
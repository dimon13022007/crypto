from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    gmail = forms.EmailField(label='Gmail')
    # Додаткові поля для форми реєстрації (необов'язково)
    # наприклад, номер телефону, дата народження тощо

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'gmail')



class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Завантажте картинку')
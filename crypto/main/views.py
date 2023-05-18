from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm

def index(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Перенаправлення після реєстрації
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправлення після входу
        else:
            # Повідомлення про помилку аутентифікації
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')















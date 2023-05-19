from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
import pytesseract
from PIL import Image
from .forms import ImageUploadForm


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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
            return render(request, 'main/login.html', {'error_message': error_message})
    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            language = request.POST.get('language')
            text = extract_text_from_image(image, language)
            return render(request, 'main/result.html', {'text': text})
    else:
        form = ImageUploadForm()
    return render(request, 'main/upload.html', {'form': form})


def extract_text_from_image(image, language):
    # Обробка картинки та отримання тексту
    img = Image.open(image)
    if language == 'eng':
        languages = 'eng'
    elif language == 'rus':
        languages = 'rus'
    elif language == 'ukr':
        languages = 'ukr'
    else:
        # За замовчуванням використовуємо всі мови
        languages = 'eng+rus+ukr'
    text = pytesseract.image_to_string(img, lang=languages)
    return text








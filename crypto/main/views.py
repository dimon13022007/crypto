from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
import pytesseract
from PIL import Image
from .forms import ImageUploadForm
import openai
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
openai.api_key = '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'

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
            return redirect('home')
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
            return redirect('home')
        else:
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
            response = get_chatgpt_response(text)
            return render(request, 'main/result.html',  {'response': response})
    else:
        form = ImageUploadForm()
    return render(request, 'main/upload.html', {'form': form})

def preprocess_text(text):
    # Удаление лишних символов и исправление ошибок
    text = re.sub(r'[^\w\s]', '', text)  # Удаление знаков препинания
    text = re.sub(r'\s+', ' ', text)  # Удаление лишних пробелов
    text = text.lower()  # Приведение к нижнему регистру
    return text


def extract_text_from_image(image, language):
    img = Image.open(image)
    if language == 'eng':
        languages = 'eng'
    elif language == 'rus':
        languages = 'rus'
    elif language == 'ukr':
        languages = 'ukr'
    else:
        languages = 'eng+rus+ukr'
    text = pytesseract.image_to_string(img, lang=languages)
    return text


def get_chatgpt_response(question):
    question = preprocess_text(question)
    prompt = "Question: " + question + "\nAnswer:"

    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=170,
        temperature=1.2,
        top_p=0.2,
        n=3,
        stop='FFFff'

    )

    if response.choices:
        answer = response.choices[0].text.strip()
        return answer
    else:
        return "Не удалось получить ответ от модели GPT-3."
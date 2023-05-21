from . import views
from django.urls import path
from .views import upload_image


urlpatterns = [
    path('', views.index, name='home'),
    path('dd/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('upload/', upload_image, name='upload_image'),





]
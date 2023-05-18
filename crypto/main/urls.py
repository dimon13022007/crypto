from . import views
from django.urls import path



urlpatterns = [
    path('', views.index, name='home'),
    path('dd/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),




]
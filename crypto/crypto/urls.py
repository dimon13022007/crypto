
from django.contrib import admin
from django.urls import path, include






urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts', include("django.contrib.auth.urls")),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard', include('jet.dashboard.urls', 'jet-dashboard')),

]


from django.contrib import admin
from django.urls import path, include

from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', HomeView.as_view(), name='home'),

    # Api
    path('api/', include('api.urls')),
]

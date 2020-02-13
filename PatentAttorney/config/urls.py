from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', HomeView.as_view(), name='app'),

    # Api
    path('api/', include('api.urls')),
]

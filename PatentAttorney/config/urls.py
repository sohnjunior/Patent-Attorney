from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    #path('', HomeView.as_view(), name='home'),

    # Api
    path('api/', include('api.urls')),


    path("",
         TemplateView.as_view(template_name="test.html"),
         name="app",
         ),

]

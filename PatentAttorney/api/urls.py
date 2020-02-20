from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    # /api/patent_image/detail
    path('patent_image/detail/', views.ApiPatentDetail.as_view(), name='patent_detail'),

    # /api/patent_image/predict
    path('patent_image/predict/', views.ApiPatentPredict.as_view(), name='patent_predict'),
]

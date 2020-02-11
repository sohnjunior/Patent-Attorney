from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    # /api/patent_image/list
    path('patent_image/list/', views.ApiPatentList.as_view(), name='patent_list'),

    # /api/patent_image/predict
    path('patent_image/predict/', views.ApiPatentPredict.as_view(), name='patent_predict'),
]

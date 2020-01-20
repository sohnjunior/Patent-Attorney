from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    # /api/patent/list
    path('patent/list/', views.ApiPatentList.as_view(), name='patent_list'),

    # /api/patent/predict
    path('patent/predict', views.ApiPatentPredict.as_view(), name='patent_predict'),
]

from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    # /api/patent/predict
    path('patent/predict/', views.PatentPredict.as_view(), name='patent_predict'),

    # /api/mark/detail
    path('mark/detail/<int:pk>/', views.MarkInfo.as_view(), name='mark_info'),

    # /api/design/detail
    path('design/detail/<int:pk>/', views.DesignInfo.as_view(), name='design_info'),
]

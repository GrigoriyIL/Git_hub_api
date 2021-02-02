from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeRepository.as_view(), name='home')
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeRepository.as_view(), name='home'),
    path('repositorys/add_repository/', views.add_repository, name='add_repository')
]
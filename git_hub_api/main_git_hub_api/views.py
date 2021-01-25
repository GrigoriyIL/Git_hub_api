from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import requests as py_request
from .models import Commit, Collaborator, RepositoryUser, Repository
from datetime import datetime

def index(request):
    RepositoryUsers = RepositoryUser.objects.all()
    Repositorys = Repository.objects.all()
    repository_url = "https://api.github.com/repos/GrigoriyIL/-Decompilation"
    response_repository = py_request.get(repository_url).json()
    login = response_repository['owner']['login']
    date = datetime.strptime(response_repository['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    if not RepositoryUser.objects.filter(name=login):
        RepositoryUsers.create(name=login, is_github_user='True')
    if not Repository.objects.filter(repository_name=response_repository['name']):
        Repositorys.create(repository_name=response_repository['name'],
                           owner=RepositoryUser.objects.get(name=login),
                           date_of_creation=datetime.strptime(response_repository['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                           repository_url=f'https://github.com/{response_repository["full_name"]}')
    return HttpResponse(Repositorys)

# def get_repository(request):
#     response = py_request.get('https://api.github.com/repos/GrigoriyIL/-Decompilation')
#     for item in response:

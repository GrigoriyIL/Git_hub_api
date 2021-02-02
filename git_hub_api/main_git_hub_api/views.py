from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
import requests as py_request
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from datetime import datetime

from .models import Commit, Collaborator, RepositoryUser, Repository


class HomeRepository(ListView):
    model = Repository
    template_name = 'main_git_hub_api/home_repository_list.html'
    context_object_name = 'repository_user'

    def get_context_data(self,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная страница'
        return context


def get_repository(request):
    # Get models
    repository_users = RepositoryUser.objects.all()
    repositorys = Repository.objects.all()
    collaborators = Collaborator.objects.all()
    commits = Commit.objects.all()
    full_repository_name = 'TelegramBot/Api'

    # Get repository URL
    repository_url = "https://api.github.com/repos/" + full_repository_name
    response_repository = py_request.get(repository_url).json()
    response_commits = py_request.get(repository_url + "/commits").json()

    # way to owner login
    login = response_repository['owner']['login']

    # Set information about users/collaborators
    if not repository_users.filter(name=login):
        repository_users.create(name=login)
    repository_user = repository_users.get(name=login)

    # Set information about repository
    date = datetime.strptime(response_repository['created_at'], '%Y-%m-%dT%H:%M:%SZ')

    if not repositorys.filter(repository_name=response_repository['name']):
        repository_user.repository_set.create(
            repository_name=response_repository['name'],
            owner= repository_user.name,
            date_of_creation= date,
            repository_url=f'https://github.com/{response_repository["full_name"]}'
        )


    for item in response_commits:
        committer_name = item["commit"]["committer"]["name"]
        commit_date = item["commit"]["committer"]["date"]
        massage = item["commit"]["message"]

        if not repository_users.filter(name=committer_name):
            repository_users.create(name=committer_name)
        repository_user = repository_users.get(name=committer_name)
        

        if not repository_user.collaborator.filter(name=repository_user.pk):
            repository_user.collaborator.create(
                name=committer_name, 
                repository=repositorys.get(repository_name=response_repository['name']),
                is_github_user =True
            )
        collab = collaborators.get(name_id=repository_user.pk)

        if not commits.filter(commit_massage=massage):
            collab.commit_set.create(
                committer=collab.pk,
                commit_massage=massage,
                commit_date=datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            )
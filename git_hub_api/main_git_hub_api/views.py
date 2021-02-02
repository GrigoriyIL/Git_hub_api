from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
import requests as py_request
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from datetime import datetime

from .models import Commit, Collaborator, RepositoryUser, Repository
from .forms import RepositoryForm


class HomeRepository(ListView):
    model = Repository
    template_name = 'main_git_hub_api/home_repository_list.html'
    context_object_name = 'repository_user'

    def get_context_data(self,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная страница'
        return context

def add_repository(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            get_repository(form.cleaned_data['repository_url']) 
#TODO: change redirect url
            return redirect('http://127.0.0.1:8000/')
    else:
        form = RepositoryForm()
    return render(request, 'main_git_hub_api/add_repository.html', {'form': form})


def get_repository(repo_link):
    # Get models
    repository_users = RepositoryUser.objects.all()
    repositorys = Repository.objects.all()
    collaborators = Collaborator.objects.all()
    commits = Commit.objects.all()
    get_global_url = repo_link.split('/')

    # Get repository URL
    repository_url = "https://api.github.com/repos/" + f'{get_global_url[-2]}/{get_global_url[-1]}'
    response_repository = py_request.get(repository_url).json()
    response_commits = py_request.get(repository_url + "/commits").json()
    if response_repository["message"] == "Not Found":
#TODO: change redirect url
        return redirect('http://127.0.0.1:8000/')
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
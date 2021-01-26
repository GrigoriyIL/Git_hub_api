from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import requests as py_request
from .models import Commit, Collaborator, RepositoryUser, Repository
from datetime import datetime


def index(request):

    return HttpResponse(get_repository(request))


def get_repository(request):
    # Get models
    repository_users = RepositoryUser.objects.all()
    repository = Repository.objects.all()
    collaborator = Collaborator.objects.all()
    commits = Commit.objects.all()

    # Get repository URL
    repository_url = "https://api.github.com/repos/GrigoriyIL/Git_hub_api"
    response_repository = py_request.get(repository_url).json()
    response_commits = py_request.get(repository_url + "/commits").json()

    # way to owner login
    login = response_repository['owner']['login']

    # Set information about users/collaborators
    if not repository_users.filter(name=login):
        repository_users.create(name=login, is_github_user='True')

    # Set information about repository
    date = datetime.strptime(response_repository['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    if not repository.filter(repository_name=response_repository['name']):
        repository.create(repository_name=response_repository['name'],
                          owner=repository_users.get(name=login),
                          date_of_creation=datetime.strptime(response_repository['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                          repository_url=f'https://github.com/{response_repository["full_name"]}'
                          )
    for item in response_commits:
        # way to committer name
        committer_name = item["commit"]["committer"]["name"]
        committer_date = item["commit"]["committer"]["date"]
        massage = item["commit"]["message"]
        # Set collaborator
        if not repository_users.filter(name=committer_name):
            repository_users.create(name=committer_name)

        if not collaborator.filter(name=repository_users.get(name=committer_name).id):
            collaborator.create(name=repository_users.get(name=committer_name),
                                repository=repository.get(repository_name=response_repository['name']),
                                is_github_user=repository_users.get(is_github_user='True')
                                )
        # Set commits
        if not commits.filter(commit_massage=massage):
            commits.create(committer=collaborator.get(name=repository_users.get(name=committer_name).id),
                           commit_massage=massage,
                           commit_date=datetime.strptime(committer_date, '%Y-%m-%dT%H:%M:%SZ')
                           )


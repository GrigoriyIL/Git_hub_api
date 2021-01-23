from django.db import models


class RepositoryUser(models.Model):
    name = models.CharField('User name', max_length=50)
    is_github_user = models.BooleanField(default='false')

    def __str__(self):
        return self.name


class Repository(models.Model):
    repository_name = models.CharField('Repository name', max_length=100)
    owner = models.ForeignKey(RepositoryUser, on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField("Date of creation")
    repository_url = models.URLField()

    def __str__(self):
        return self.repository_name


class Collaborator(models.Model):
    name = models.ForeignKey(RepositoryUser, on_delete=models.CASCADE, related_name='user_name')
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    is_github_user = models.ForeignKey(RepositoryUser, on_delete=models.CASCADE, related_name='is_github_collaborator')

    def __str__(self):
        return f'{self.name}'


class Commit(models.Model):
    committer = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    commit_massage = models.CharField('Comment text', max_length=200)
    commit_date = models.DateTimeField("Date of commit")

    def __str__(self):
        return self.commit_massage

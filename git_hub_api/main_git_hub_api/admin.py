from django.contrib import admin

from .models import RepositoryUser, Repository, Commit, Collaborator


class RepositoryUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'repository_name', 'owner', 'repository_url', 'date_of_creation')


class CommitAdmin(admin.ModelAdmin):
    list_display = ('id', 'committer', 'commit_massage', 'commit_date')


class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'repository', 'is_github_user')


admin.site.register(RepositoryUser, RepositoryUserAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)

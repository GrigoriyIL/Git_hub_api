from django.db import models


class RepositoryUser(models.Model):
    name = models.CharField('Логин', max_length=50)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Польователь репозитория'
        verbose_name_plural='Пользователи репозитория'



class Repository(models.Model):
    repository_name = models.CharField('Название репозитория', max_length=100)
    owner = models.ForeignKey(RepositoryUser, on_delete=models.CASCADE, verbose_name='Создатель')
    date_of_creation = models.DateTimeField("Дата создания")
    repository_url = models.URLField(verbose_name='Ссылка на репозиторий')

    def __str__(self):
        return self.repository_name

    class Meta:
        verbose_name='Репозиторий'
        verbose_name_plural='Репозитории'



class Collaborator(models.Model):
    name = models.ForeignKey(RepositoryUser, on_delete=models.CASCADE, related_name='collaborator', verbose_name='Логин')
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, verbose_name='Репозиторий')
    is_github_user = models.BooleanField(default=False, verbose_name='Пользователь Github?')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name='Соавтор'
        verbose_name_plural='Соавторы'


class Commit(models.Model):
    committer = models.ForeignKey(Collaborator, on_delete=models.CASCADE, verbose_name='Автор')
    commit_massage = models.CharField('Сообщение', max_length=200)
    commit_date = models.DateTimeField("Дата создания")

    def __str__(self):
        return self.commit_massage

    class Meta:
        verbose_name='Коммит'
        verbose_name_plural='Коммиты'
        ordering = ['-commit_date']


from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType

class NotesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title  = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notes'

class TodoModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Todo'

class HomeworkModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return self.title
    
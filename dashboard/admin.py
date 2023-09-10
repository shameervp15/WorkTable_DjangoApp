from django.contrib import admin

from .models import HomeworkModels, NotesModel, TodoModel


admin.site.register(NotesModel)
admin.site.register(HomeworkModels)
admin.site.register(TodoModel)

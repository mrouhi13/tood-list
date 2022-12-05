from django.contrib import admin

from apps.tasks.models import Task

admin.site.register(Task)

from django.contrib import admin

from apps.projects.models import Member, Project

admin.site.register(Project)
admin.site.register(Member)

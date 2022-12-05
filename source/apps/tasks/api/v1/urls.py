from django.urls import include, path

from apps.tasks.api.v1.views import TaskViewSet
from core.routers import ProjectsRouter

app_name = 'tasks'

projects_router = ProjectsRouter()
projects_router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(projects_router.urls)),
]

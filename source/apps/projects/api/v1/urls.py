from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.projects.api.v1.views import ProjectViewSet

app_name = 'projects'

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import include, path

app_name = 'api_v1'

urlpatterns = [
    path('', include('apps.projects.api.v1.urls')),
    path('', include('apps.tasks.api.v1.urls')),
    path('user/', include('apps.users.api.v1.urls', namespace='users')),
]

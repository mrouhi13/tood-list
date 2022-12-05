from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('base.api_urls.v1', namespace='api_v1')),
]

if settings.DEBUG:
    from rest_framework.documentation import include_docs_urls

    urlpatterns += [
        path('api-auth/',
             include('rest_framework.urls', namespace='rest_framework')),
        path('docs/', include_docs_urls(
            title='Tood List API',
            description='Tood List API '
                        f'{settings.REST_FRAMEWORK["DEFAULT_VERSION"]}',
            permission_classes=[AllowAny])),
    ]

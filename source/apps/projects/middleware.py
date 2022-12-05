from django.http import Http404

from apps.projects.models import Project


class AddProjectObjectToRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_parts = request.path.split('/')
        request.project = None
        if len(path_parts) >= 3:
            project_id = path_parts[2]

            if path_parts[2] == 'projects':
                project_id = path_parts[3] if path_parts[3] else None

            try:
                request.project = Project.objects.get(
                    pk=int(project_id),
                ) if project_id else None
            except Project.DoesNotExist:
                raise Http404
            except ValueError:
                pass

        return self.get_response(request)

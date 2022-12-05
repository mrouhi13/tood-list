from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.projects.constants import MemberRole
from apps.projects.models import Member, Project

User = get_user_model()


class TasksAPITests(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user('user_1', password='1234')

        self.client.login(username='user_1', password='1234')

    def test_list_projects(self):
        project_1 = Project.objects.create(title='Test 1')
        project_2 = Project.objects.create(title='Test 2')
        Project.objects.create(title='Test 3')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.MANAGER)
        Member.objects.create(user=self.user_1, project=project_2,
                              role=MemberRole.DEVELOPER)

        url = reverse('api_v1:projects:project-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], project_1.title)
        self.assertEqual(response.data['results'][1]['title'], project_2.title)

    def test_create_project(self):
        url = reverse('api_v1:projects:project-list')
        data = {
            'title': 'test',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_add_member(self):
        project_1 = Project.objects.create(title='Test 1')
        user_2 = User.objects.create_user('user_2', password='1234')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.MANAGER)

        url = reverse('api_v1:projects:project-add-member',
                      kwargs={'pk': project_1.pk})
        data = {
            'user': user_2.pk,
            'role': MemberRole.DEVELOPER,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_member_with_duplicate_member(self):
        project_1 = Project.objects.create(title='Test 1')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.MANAGER)

        url = reverse('api_v1:projects:project-add-member',
                      kwargs={'pk': project_1.pk})
        data = {
            'user': self.user_1.pk,
            'role': MemberRole.DEVELOPER,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'The field user and project must make a unique set.')

    def test_add_member_without_permission(self):
        user_2 = User.objects.create_user('user_2', password='1234')
        project_1 = Project.objects.create(title='Test 1')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.DEVELOPER)

        url = reverse('api_v1:projects:project-add-member',
                      kwargs={'pk': project_1.pk})
        data = {
            'user': user_2.pk,
            'role': MemberRole.DEVELOPER,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

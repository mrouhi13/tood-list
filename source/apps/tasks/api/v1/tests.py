from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.projects.constants import MemberRole
from apps.projects.models import Member, Project
from apps.tasks.models import Task

User = get_user_model()


class TaskAPITests(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user('user_1', password='1234')

        self.client.login(username='user_1', password='1234')

    def test_list_tasks(self):
        project_1 = Project.objects.create(title='Test 1')
        project_2 = Project.objects.create(title='Test 2')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.MANAGER)
        Member.objects.create(user=self.user_1, project=project_2,
                              role=MemberRole.DEVELOPER)
        task_1 = Task.objects.create(title='Test 1', project=project_1)
        Task.objects.create(title='Test 2', project=project_2)

        url = reverse('api_v1:tasks:task-list',
                      kwargs={'project_pk': project_1.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], task_1.title)

    def test_list_tasks_without_permission(self):
        project_1 = Project.objects.create(title='Test 1')
        Task.objects.create(title='Test 1', project=project_1)

        url = reverse('api_v1:tasks:task-list',
                      kwargs={'project_pk': project_1.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_with_manager_role(self):
        user_2 = User.objects.create_user('user_2', password='1234')
        project_1 = Project.objects.create(title='Test 1')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.MANAGER)
        member_2 = Member.objects.create(user=user_2, project=project_1,
                                         role=MemberRole.MANAGER)

        url = reverse('api_v1:tasks:task-list',
                      kwargs={'project_pk': project_1.pk})
        data = {
            'title': 'test',
            'assignees': [member_2.pk],
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['assignees'][0], member_2.pk)

    def test_create_task_with_developer_role(self):
        user_2 = User.objects.create_user('user_2', password='1234')
        project_1 = Project.objects.create(title='Test 1')
        member_1 = Member.objects.create(user=self.user_1, project=project_1,
                                         role=MemberRole.DEVELOPER)
        member_2 = Member.objects.create(user=user_2, project=project_1,
                                         role=MemberRole.MANAGER)

        url = reverse('api_v1:tasks:task-list',
                      kwargs={'project_pk': project_1.pk})
        data = {
            'title': 'test',
            'assignees': [member_2.pk],
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['assignees'][0], member_1.pk)

    def test_create_task_with_assignee_not_member(self):
        user_2 = User.objects.create_user('user_2', password='1234')
        project_1 = Project.objects.create(title='Test 1')
        project_2 = Project.objects.create(title='Test 2')
        Member.objects.create(user=self.user_1, project=project_1,
                              role=MemberRole.DEVELOPER)
        member_1 = Member.objects.create(user=user_2, project=project_2,
                                         role=MemberRole.MANAGER)

        url = reverse('api_v1:tasks:task-list',
                      kwargs={'project_pk': project_1.pk})
        data = {
            'title': 'test',
            'assignees': [member_1.pk],
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['assignees'][0].code, 'does_not_exist')

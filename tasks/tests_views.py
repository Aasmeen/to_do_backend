import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from tasks.models import Tasks
from tasks.serializers import TaskSerializer

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', first_name='User', last_name='Test' , password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        incomplete_task_data = {'title': 'Test Task1', 'user_id': self.user.id}
        Tasks.objects.create(**incomplete_task_data)
        complete_important_task_data = {'title': 'Test Task2', 'user_id': self.user.id, 'is_completed': True, 'is_important': True}
        Tasks.objects.create(**complete_important_task_data)
        Tasks.objects.create(**complete_important_task_data)
        self.url = '/api/base/'
    
    def test_get_basic_details(self):
        # Test GET request to retrieve user basic details
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['incomplete_task'], Tasks.objects.filter(user_id=self.user.id, is_completed=False).count())
        self.assertEqual(data['important_task'], Tasks.objects.filter(user_id=self.user.id, is_important=True).count())



class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.task_data = {'title': 'Test Task', 'user_id': self.user.id}
        self.task = Tasks.objects.create(**self.task_data)
        self.url = '/api/task/'

    def test_get_all_tasks(self):
        # Test GET request to retrieve all tasks
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'incomplete_task': TaskSerializer(Tasks.objects.filter(user_id=self.user.id, is_completed=False), many=True).data,
            'complete_task': TaskSerializer(Tasks.objects.filter(user_id=self.user.id, is_completed=True), many=True).data
        }
        self.assertEqual(response.data, expected_data)

    def test_get_single_task(self):
        # Test GET request to retrieve a single task
        response = self.client.get(f'{self.url}{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = TaskSerializer(self.task).data
        self.assertEqual(response.data, expected_data)

    def test_create_task(self):
        # Test POST request to create a new task
        new_data = {'title': 'New Test Task', 'user_id': self.user.id}
        response = self.client.post(self.url, data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], new_data['title'])
        self.assertTrue(Tasks.objects.filter(title=new_data['title']).exists())

    def test_update_task(self):
        # Test PATCH request to update an existing task
        updated_data = {'title': 'Updated Test Task', 'is_completed': True, 'is_important': True}
        response = self.client.patch(f'{self.url}{self.task.id}/', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])
        self.assertEqual(response.data['is_completed'], updated_data['is_completed'])
        self.assertEqual(response.data['is_important'], updated_data['is_important'])
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, updated_data['title'])
        self.assertEqual(self.task.is_completed, updated_data['is_completed'])
        self.assertEqual(self.task.is_important, updated_data['is_important'])

    def test_delete_task(self):
        # Test DELETE request to delete an existing task
        response = self.client.delete(f'{self.url}{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tasks.objects.filter(id=self.task.id).exists())

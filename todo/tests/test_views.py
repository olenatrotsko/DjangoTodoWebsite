from django.urls import reverse
from todo.models import Todo
from utils.setup_test import TestSetup


class TestModel(TestSetup):

    def test_should_create_todo(self):
        user = self.create_test_user()
        self.client.post(reverse("login"), {
            'username': 'testuser',
            'password': 'password123'
        })

        todos = Todo.objects.all()

        self.assertEqual(len(todos), 0)

        response = self.client.post(reverse('create-todo'),{
            'title': 'Test Todo',
            'description': 'Test Description',
            'owner': user.id
        })

        updated_todos = Todo.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_todos.count(), 1)
        
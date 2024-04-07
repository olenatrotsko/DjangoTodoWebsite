from django.test import TestCase
from authentication.models import User
from ..models import Todo

class TestModels(TestCase):
    def test_should_create_todo(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
        )
        user.set_password('password123')
        user.save()

        todo = Todo(
            title='Test Todo',
            description='Test Description',
            owner=user
        )
        todo.save()

        self.assertEqual(str(todo), 'Test Todo')

            
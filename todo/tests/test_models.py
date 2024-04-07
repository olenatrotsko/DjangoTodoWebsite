from utils.setup_test import TestSetup
from ..models import Todo

class TestModels(TestSetup):
    def test_should_create_todo(self):
        user = self.create_test_user()

        todo = Todo(
            title='Test Todo',
            description='Test Description',
            owner=user
        )
        todo.save()

        self.assertEqual(str(todo), 'Test Todo')

from django.test import TestCase

from authentication.models import User

class TestSetup(TestCase):

    def setUp(self):

        self.user = {
            "username": 'testuser',
            "email": 'testuser@email.com',
            "password": 'password123',
            "password2": 'password123',
            "is_email_verified": True
        }

        return super().setUp()
    
    
    def create_test_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            is_email_verified=True
        )
        user.set_password('password123')
        user.save()

        return user
    

    def create_test_user_two(self):
        user = User.objects.create_user(
            username='testuser2',
            email='testuser2@email.com',
            is_email_verified=True
        )
        user.set_password('password123')
        user.save()

        return user


    def tearDown(self):
        return super().tearDown()
    
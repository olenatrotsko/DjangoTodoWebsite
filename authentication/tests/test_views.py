from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from utils.setup_test import TestSetup

class TestViews(TestSetup):
    def test_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')

    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
    
    def test_should_signup_user(self):
        response = self.client.post(reverse('register'), self.user)
        self.assertEqual(response.status_code, 302)

    def test_should_not_signup_user_with_taken_username(self):
        self.client.post(reverse('register'), self.user)
        response = self.client.post(reverse('register'), self.user)
        self.assertEqual(response.status_code, 409)

        storage = get_messages(response.wsgi_request)
        self.assertIn('Username is already taken', [message.message for message in storage])


    def test_should_not_signup_user_with_taken_email(self):
        self.user2 = {
            'username': 'testuser2',
            'email': 'test@gmail.com',
            'password': 'password123',
            'password2': 'password123',
        }
        self.client.post(reverse('register'), self.user)
        response = self.client.post(reverse('register'), self.user2)
        self.assertEqual(response.status_code, 409)
   
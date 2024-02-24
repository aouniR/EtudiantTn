from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from django.contrib.auth.decorators import login_required

class MyViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_my_protected_view(self):
        # Ensure unauthenticated user is redirected to login
        response = self.client.get(reverse('my_protected_view'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        # Ensure authenticated user can access the view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('my_protected_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'unauthorizedUsers.html')

    def test_error_cand_view(self):
        # Ensure unauthenticated user is redirected to login
        response = self.client.get(reverse('error_cand_view'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        # Ensure authenticated user can access the view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('error_cand_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error_cand.html')

from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from locust import HttpUser, task, between
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_student_url = reverse('register_student')
        self.register_recruiter_url = reverse('register_recruiter')
        self.registration_confirmation_url = reverse('registration_confirmation')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')

    def test_register_student_view(self):
        response = self.client.get(self.register_student_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register_student.html')

    def test_register_recruiter_view(self):
        response = self.client.get(self.register_recruiter_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register_recruiter.html')

    def test_registration_confirmation_view(self):
        response = self.client.get(self.registration_confirmation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration_confirmation.html')

    def test_user_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

class TestFunctional (TestViews):
    def test_register_student_valid_form(self):
        response = self.client.post(self.register_student_url, {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'zip_code': '12345',
            'phone': '555-555-5555'
        })
        self.assertEqual(response.status_code, 200)  

    def test_register_student_invalid_form(self):
        response = self.client.post(self.register_student_url, {
            'email': 'invalidemail',  
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'zip_code': '12345',
            'phone': '555-555-5555'
        })
        self.assertEqual(response.status_code, 200)  

class MyUser(HttpUser):
    wait_time = between(1, 3)
    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
    @task
    def register_student(self):
        response = self.client.post(self.register_student_url, {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'zip_code': '12345',
            'phone': '555-555-5555'
        })

    @task
    def login(self):
        self.client.post("/login", {"email": "test@example.com", "password": "testpassword"})

    @task
    def view_dashboard(self):
        self.client.get("/dashboard")

    @task
    def view_profile(self):
        self.client.get("/profile")

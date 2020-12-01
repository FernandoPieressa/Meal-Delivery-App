from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestRegisterView(TestCase):
    """Tests for the register view"""
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('MealDelivery:register')

    def test_register_not_logged_user(self):
        """User should be redirected if tried to get into the view without
        logging in"""
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 302)

    def test_register_get(self):
        """Should render register template if logged user"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MealDelivery/components/session/register.html')

    def test_register_post(self):
        """Should add new user if post method"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        new_username = 'new_username'
        response = self.client.post(self.register_url, {
            'username': [new_username],
            'password1': ['654321654a'],
            'password2': ['654321654a']
        })

        created_user = User.objects.get(username=new_username)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(created_user.username, new_username)

    def test_register_post_invalid(self):
        """Should render register view if invalid creation"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        response = self.client.post(self.register_url, {})

        self.assertEqual(response.status_code, 200)

class TestLoginView(TestCase):
    """Tests for the login view"""
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('MealDelivery:login')
        self.user = User.objects.create_user(username='username',
                                             password='password')

    def test_login_get(self):
        """Should render the login view"""

        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MealDelivery/components/session/login.html')

    def test_login_post(self):
        """Should login user if existing user"""

        response = self.client.post(self.login_url, {
            'username': ['username'],
            'password': ['password']
        })

        self.assertEqual(response.status_code, 302)

    def test_login_post_invalid(self):
        """Should not login user if not existing user"""

        response = self.client.post(self.login_url, {
            'username': ['username'],
            'password': ['fakepassword']
        })

        self.assertEqual(response.status_code, 200)

class TestLogoutView(TestCase):
    """Tests for the logout view"""
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('MealDelivery:logout')

    def test_logout_post(self):
        """Should render register template if logged user"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 302)

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test101@husteen.com'
        password = "TestHusteen@144"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            last_name='Smith',
            phone_number='07033562524',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen'
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@husteen.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password='password@123123',
            last_name='Smith',
            phone_number='07033562544',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testing147')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@husteen.com',
            'test147'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin201@husteen.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test456@husteen.com',
            password='password@123',
            last_name='Smith',
            phone_number='07033566534',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen'
            )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:accounts_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:accounts_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:accounts_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


class publicUserApiTest(TestCase):
    """Test the user api public"""

    def setUp(self):
        self.client = APIClient()

        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@husteen.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@husteen.com',
            password='password123',
            last_name='Smith',
            phone_number='07033562534',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen')

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'create-token@husteen.com',
            'password': 'test@test123',
            'first_name': 'Husteen',
            'last_name': 'Smith',
            'phone_number': '07063562533',
            'state': 'Lagos',
            'address': 'Lagos, Nigeria',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invallid credentials are given."""
        email = 'invalid-token@husteen.com'
        create_user(email=email,
                    password='password123',
                    last_name='Smith',
                    phone_number='07033562534',
                    state='Lagos',
                    address='Lagos, Nigeria',
                    first_name='Husteen')
        payload = {
            'email': email,
            'password': 'test@test123',
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist."""
        payload = {
            'email': 'no-user@husteen.com',
            'password': 'test@test123',
            'first_name': 'Husteen',
            'last_name': 'Smith',
            'phone_number': '07063562533',
            'state': 'Lagos',
            'address': 'Lagos, Nigeria',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'one', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class privateUserApiTest(TestCase):
    """Test the authenticated url User API"""
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin-user@husteen.com',
            password='password@123',
            last_name='Smith',
            phone_number='07033562534',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen'
        )

        self.user = get_user_model().objects.create_user(
            email='test@husteen.com',
            password='password@123',
            last_name='Smith',
            phone_number='07033562534',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen'
            )

        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.client.force_authenticate(self.admin_user)

    def test_user_exists(self):
        """Test creating user that already exists"""
        payload = {
            'email': 'user-exist@husteen.com',
            'password': 'test@test123',
            'first_name': 'Husteen',
            'last_name': 'Smith',
            'phone_number': '07033562533',
            'state': 'Lagos',
            'address': 'Lagos, Nigeria',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test-user@husteen.com',
            'password': 'pw',
            'first_name': 'Husteen',
            'last_name': 'Smith',
            'phone_number': '07033562534',
            'state': 'Lagos',
            'address': 'Lagos, Nigeria',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@test123',
            'first_name': 'Husteen',
            'last_name': 'Smith',
            'phone_number': '07033562534',
            'state': 'Lagos',
            'address': 'Lagos, Nigeria',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

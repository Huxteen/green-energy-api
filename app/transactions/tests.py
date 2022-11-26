from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from transactions.models import Transaction
from products.models import Product
import uuid
ref = uuid.uuid4().hex
ref_2 = uuid.uuid4().hex


CREATE_TRANSACTION_URL = reverse('create-transaction')
VALIDATE_TRANSACTION_URL = reverse('validate-transaction', args=[ref])
RETRIEVE_TRANSACTION_URL = reverse('retrieve-transaction', args=[ref])
CUSTOMER_TRANSACTION_URL = reverse('customer-transaction')
LIST_CUSTOMER_TRANSACTION_URL = reverse('list-customer-transaction')


# Create your tests here.
class publicTransactionApiTest(TestCase):
    """Test the Transaction api public"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_create_transaction(self):
        """Test that login is required to create Transaction"""
        res = self.client.post(CREATE_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_validate_transaction(self):
        """Test that login is required to validate Transaction"""
        res = self.client.put(VALIDATE_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_retrieve_transaction(self):
        """Test that login is required to retrieve Transaction"""
        res = self.client.get(RETRIEVE_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_customer_transaction(self):
        """Test that login is required to retrieve customer Transaction"""
        res = self.client.get(CUSTOMER_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_list_customer_transaction(self):
        """Test that login is required to retrieve customer Transaction"""
        res = self.client.get(LIST_CUSTOMER_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateTransactionApiTest(TestCase):
    """Test the authorized Transaction API"""
    def setUp(self):
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

        self.product = Product.objects.create(
            user_id=self.user,
        )

        self.user_2 = get_user_model().objects.create_user(
            email='test2@husteen.com',
            password='password@123',
            last_name='Smith',
            phone_number='07033562534',
            state='Lagos',
            address='Lagos, Nigeria',
            first_name='Husteen'
        )

        self.product_2 = Product.objects.create(
            user_id=self.user_2,
        )

        self.transaction = Transaction.objects.create(
            amount=100000,
            payment_channel='paystack',
            product_id=self.product,
            user_id=self.user,
            reference=ref,
        )
        self.transaction_2 = Transaction.objects.create(
            amount=100000,
            payment_channel='paystack',
            product_id=self.product,
            user_id=self.user,
            reference=ref_2,
        )

    def test_validate_users_transactions(self):
        """Test validate users transactions"""
        res = self.client.put(VALIDATE_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'success')
        self.assertTrue(res.data['is_active'])
        self.assertEqual(res.data['reference'], ref)

    def test_create_transactions_successful(self):
        """Test create transaction successful"""
        payload = {
            "amount": 500000,
            "payment_channel": 'paystack',
        }
        res = self.client.post(CREATE_TRANSACTION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['payment_channel'],
                         payload['payment_channel'])

    def test_retrieve_users_transactions(self):
        """Test retrieve users Transactions"""
        res = self.client.get(RETRIEVE_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['reference'], ref)

    def test_retrieve_all_customer_transactions(self):
        """Test retrieve all customer Transactions"""
        res = self.client.get(CUSTOMER_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual((res.data['count']), 2)

    def test_retrieve_all_transactions(self):
        """Test retrieve all Transactions"""
        res = self.client.get(LIST_CUSTOMER_TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual((res.data['count']), 2)

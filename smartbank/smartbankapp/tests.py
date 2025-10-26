import io
import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from smartbankapp.models import Customer


class KycCreateAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and token for authentication
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()

        # Auth header
        self.auth_header = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        # Create sample customer for GET & update tests
        self.customer = Customer.objects.create(
            customer_name='John Doe',
            email='john@example.com',
            id_type=1,
            id_document='dummy.pdf',
            address='123 Street',
            city='Chennai',
            state='TN',
            pincode='600001',
        )

    def test_unauthorized_access(self):
        """Check if API denies access without token"""
        url = '/kyc_create'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_create_customer_success(self):
        """Create new customer successfully"""
        url = '/kyc_create'
        test_file = SimpleUploadedFile("test_id.pdf", b"dummy content", content_type="application/pdf")
        data = {
            'data': json.dumps({
                'name': 'Jane Doe',
                'email': 'jane@example.com',
                'id_type': 1,
                'address': '456 Road',
                'city': 'Bangalore',
                'state': 'KA',
                'pincode': '560001'
            }),
            'id_document': test_file
        }

        response = self.client.post(url, data, format='multipart', **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully Created', response.content.decode())

    def test_create_customer_invalid_file_type(self):
        """File extension not allowed"""
        url = '/kyc_create'
        bad_file = SimpleUploadedFile("test.txt", b"not allowed", content_type="text/plain")
        data = {
            'data': json.dumps({
                'name': 'Mark',
                'email': 'mark@example.com',
                'id_type': 1,
                'address': 'Delhi',
                'city': 'Delhi',
                'state': 'DL',
                'pincode': '110001'
            }),
            'id_document': bad_file
        }

        response = self.client.post(url, data, format='multipart', **self.auth_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn('File type in pdf or jpg or jpeg', response.content.decode())

    def test_get_customer_details(self):
        """Fetch existing customer details"""
        url = f'/kyc_create?cus_id={self.customer.id}'
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', response.content.decode())

    def test_update_customer(self):
        """Update existing customer"""
        url = '/kyc_create'
        update_file = SimpleUploadedFile("update.pdf", b"update content", content_type="application/pdf")
        data = {
            'data': json.dumps({
                'id': self.customer.id,
                'name': 'John Updated',
                'email': 'johnupdated@example.com',
                'id_type': 2,
                'address': 'New Street',
                'city': 'Coimbatore',
                'state': 'TN',
                'pincode': '641001'
            }),
            'id_document': update_file
        }

        response = self.client.post(url, data, format='multipart', **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully Updated', response.content.decode())

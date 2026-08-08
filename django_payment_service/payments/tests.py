from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

class PaymentApiTestCase(TestCase):
    def setUp(self):
        self.create_link_url = reverse('create-payment-link')

    @patch('stripe.checkout.Session.create')
    def test_create_stripe_payment_link_success(self, mock_stripe_create):
        # Setup Stripe Session mock url return
        class MockSession:
            url = 'https://checkout.stripe.com/c/pay/cs_test_mockurl123'
        mock_stripe_create.return_value = MockSession()

        payload = {
            "order_id": 12345,
            "amount": 9900,  # $99.00
            "currency": "USD",
            "gateway": "stripe"
        }
        
        response = self.client.post(self.create_link_url, payload, content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['gateway'], 'stripe')
        self.assertEqual(response.json()['payment_link'], 'https://checkout.stripe.com/c/pay/cs_test_mockurl123')
        mock_stripe_create.assert_called_once()

    @patch('razorpay.Client')
    def test_create_razorpay_payment_link_success(self, mock_razorpay_client_class):
        # Mock the Razorpay Client and its method chain: client.payment_link.create
        mock_client_instance = mock_razorpay_client_class.return_value
        mock_client_instance.payment_link.create.return_value = {
            "short_url": "https://rzp.io/i/mockrzpurl"
        }

        payload = {
            "order_id": 67890,
            "amount": 49900,  # ₹499.00
            "currency": "INR",
            "gateway": "razorpay"
        }

        response = self.client.post(self.create_link_url, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['gateway'], 'razorpay')
        self.assertEqual(response.json()['payment_link'], 'https://rzp.io/i/mockrzpurl')
        mock_client_instance.payment_link.create.assert_called_once()

    def test_create_payment_link_missing_fields(self):
        payload = {
            "order_id": 12345,
            "gateway": "stripe"
            # Missing amount
        }
        response = self.client.post(self.create_link_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount is required', response.json()['error'])

    def test_create_payment_link_invalid_gateway(self):
        payload = {
            "order_id": 12345,
            "amount": 1000,
            "gateway": "invalid_gateway"
        }
        response = self.client.post(self.create_link_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Unsupported payment gateway', response.json()['error'])

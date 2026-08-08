from abc import ABC, abstractmethod
import stripe
import razorpay
from django.conf import settings

class PaymentService(ABC):
    @abstractmethod
    def generate_payment_link(self, order_id: int, amount: int, currency: str) -> str:
        """
        Generates a payment link/session URL for the specified order.
        
        Args:
            order_id (int): The ID of the order.
            amount (int): The amount in the smallest currency subunit (e.g. cents for USD, paise for INR).
            currency (str): The 3-letter ISO currency code.
            
        Returns:
            str: The payment gateway checkout or payment link URL.
        """
        pass


class StripePaymentService(PaymentService):
    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY

    def generate_payment_link(self, order_id: int, amount: int, currency: str) -> str:
        try:
            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'product_data': {
                            'name': f"Order #{order_id}",
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/api/payments/success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:8000/api/payments/cancel/',
                metadata={
                    'order_id': order_id,
                }
            )
            return session.url
        except Exception as e:
            raise Exception(f"Stripe Payment Session creation failed: {str(e)}")


class RazorpayPaymentService(PaymentService):
    def __init__(self):
        # Initialize Razorpay Client with credentials
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def generate_payment_link(self, order_id: int, amount: int, currency: str) -> str:
        try:
            # Create Razorpay Payment Link
            payment_link_data = {
                "amount": amount,
                "currency": currency.upper(),
                "accept_partial": False,
                "reference_id": f"order_{order_id}",
                "description": f"Payment for Order #{order_id}",
                "customer": {
                    "name": "Guest Customer",
                    "email": "customer@example.com",
                    "contact": "+919876543210"
                },
                "notify": {
                    "sms": False,
                    "email": True
                },
                "reminder_enable": True,
                "callback_url": "http://localhost:8000/api/payments/callback/",
                "callback_method": "get"
            }
            payment_link = self.client.payment_link.create(data=payment_link_data)
            return payment_link.get('short_url')
        except Exception as e:
            raise Exception(f"Razorpay Payment Link creation failed: {str(e)}")


class PaymentServiceFactory:
    @staticmethod
    def get_payment_service(gateway: str) -> PaymentService:
        gateway = gateway.lower()
        if gateway == 'stripe':
            return StripePaymentService()
        elif gateway == 'razorpay':
            return RazorpayPaymentService()
        else:
            raise ValueError(f"Unsupported payment gateway: '{gateway}'. Supported gateways: 'stripe', 'razorpay'.")

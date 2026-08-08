from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from payments.services import PaymentServiceFactory

class CreatePaymentLinkView(APIView):
    """
    API endpoint to generate payment links for a specific order using a selected gateway.
    
    Accepts POST requests with payload:
    - order_id: Integer (Required)
    - amount: Integer (Required, in subunit e.g. cents/paise)
    - currency: String (Optional, e.g. "USD", "INR", defaults to "USD")
    - gateway: String (Required, either 'stripe' or 'razorpay')
    """
    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'USD')
        gateway = request.data.get('gateway')

        # Basic validations
        if order_id is None:
            return Response({"error": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        if amount is None:
            return Response({"error": "amount is required (in cents/paise)"}, status=status.HTTP_400_BAD_REQUEST)
        if not gateway:
            return Response({"error": "gateway is required ('stripe' or 'razorpay')"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            order_id = int(order_id)
        except ValueError:
            return Response({"error": "order_id and amount must be numeric integers"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch corresponding PaymentService implementation and generate link
            payment_service = PaymentServiceFactory.get_payment_service(gateway)
            payment_link = payment_service.generate_payment_link(order_id, amount, currency)
            
            return Response({
                "success": True,
                "gateway": gateway.lower(),
                "order_id": order_id,
                "amount": amount,
                "currency": currency.upper(),
                "payment_link": payment_link
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Simple mock endpoints for redirection testing
def payment_success(request):
    session_id = request.GET.get('session_id', 'N/A')
    return HttpResponse(
        f"<html><body>"
        f"<h2 style='color: green;'>Payment Successful!</h2>"
        f"<p>Thank you for your purchase. Session ID: {session_id}</p>"
        f"</body></html>"
    )

def payment_cancel(request):
    return HttpResponse(
        f"<html><body>"
        f"<h2 style='color: red;'>Payment Cancelled</h2>"
        f"<p>The transaction was cancelled by the user.</p>"
        f"</body></html>"
    )

def payment_callback(request):
    return HttpResponse(
        f"<html><body>"
        f"<h2 style='color: blue;'>Payment Callback</h2>"
        f"<p>Callback webhook trigger processed successfully.</p>"
        f"</body></html>"
    )

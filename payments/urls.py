from django.urls import path
from payments.views import CreatePaymentLinkView, payment_success, payment_cancel, payment_callback

urlpatterns = [
    path('create-link/', CreatePaymentLinkView.as_view(), name='create-payment-link'),
    path('success/', payment_success, name='payment-success'),
    path('cancel/', payment_cancel, name='payment-cancel'),
    path('callback/', payment_callback, name='payment-callback'),
]

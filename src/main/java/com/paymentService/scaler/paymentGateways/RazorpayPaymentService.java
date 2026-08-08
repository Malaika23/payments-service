package com.paymentService.scaler.paymentGateways;

import org.springframework.stereotype.Service;

import com.paymentService.scaler.services.PaymentService;

@Service
public class RazorpayPaymentService implements PaymentService {

    @Override
    public String generatePaymentLink(long orderId) {
        return "razorpay";
    }

}

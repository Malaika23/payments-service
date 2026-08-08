package com.paymentService.scaler.controllers;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import com.paymentService.scaler.services.PaymentService;

@RestController
public class PaymentController {

    // We are creating a payment link using 3rd parties like Razorpay,Stripe,etc.

    private PaymentService paymentService;

    public PaymentController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @PostMapping("/payments")
    public String generatePaymentLink() {
        return "generatepaymentLink";
    }

}

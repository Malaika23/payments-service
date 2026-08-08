package com.paymentService.scaler.services;

public interface PaymentService {
    // can have multiple implementations
    public String generatePaymentLink(long orderId);

}

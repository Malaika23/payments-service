# Django Payment Service with Stripe and Razorpay Integration

This is a Django-based backend microservice that integrates Stripe and Razorpay gateways to generate payment links dynamically using a factory/strategy design pattern.

## Directory Structure

```text
django_payment_service/
│
├── payment_service/        # Django Project Configuration
│   ├── settings.py         # Includes CorsHeaders, DRF, and Gateway settings
│   └── urls.py             # Main routing mapping to payments app urls
│
├── payments/               # Django App for processing payments
│   ├── services.py         # Strategy Pattern implementations for Stripe/Razorpay
│   ├── views.py            # API View and Redirect Views (success, cancel, callback)
│   └── urls.py             # Local routes for the payments app
│
├── requirements.txt        # Dependencies (Django, Stripe, Razorpay, python-dotenv)
├── .env                    # Key configurations (Stripe keys, Razorpay keys)
└── manage.py               # Django management script
```

---

## Installation & Setup

### 1. Prerequisites
Ensure Python 3.8+ is installed on your local machine.

### 2. Create and Activate Virtual Environment
```bash
# Navigate to the django_payment_service directory
cd django_payment_service

# Create venv
python -m venv venv

# Activate venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Windows Cmd:
.\venv\Scripts\activate.bat

# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Open the `.env` file in the root of the project and replace the placeholders with your API keys:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True

STRIPE_API_KEY=sk_test_...your_stripe_key_here
STRIPE_WEBHOOK_SECRET=whsec_...your_stripe_webhook_secret_here

RAZORPAY_KEY_ID=rzp_test_...your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=...your_razorpay_key_secret_here
```

### 5. Initialize Database & Run Server
Run the standard Django setup checks and run the server:
```bash
python manage.py migrate
python manage.py runserver
```
The server will start on `http://127.0.0.1:8000/`.

---

## API Documentation

### Create Payment Link
Generates a redirectable payment link using the specified gateway.

* **URL**: `/api/payments/create-link/`
* **Method**: `POST`
* **Headers**: `Content-Type: application/json`
* **Payload Structure**:
  ```json
  {
    "order_id": 1001,
    "amount": 5000,
    "currency": "USD",
    "gateway": "stripe"
  }
  ```
  *(Note: `amount` must be in the smallest currency subunit. For USD, 5000 = $50.00. For INR, 5000 = ₹50.00)*

* **Response Example (Success - 201 Created)**:
  ```json
  {
    "success": true,
    "gateway": "stripe",
    "order_id": 1001,
    "amount": 5000,
    "currency": "USD",
    "payment_link": "https://checkout.stripe.com/c/pay/cs_test_..."
  }
  ```

---

## Verification & Manual Testing

You can use `curl` or Postman to test the generation endpoint.

### Testing Stripe Link
```bash
curl -X POST http://127.0.0.1:8000/api/payments/create-link/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1001, "amount": 1000, "currency": "USD", "gateway": "stripe"}'
```

### Testing Razorpay Link
```bash
curl -X POST http://127.0.0.1:8000/api/payments/create-link/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1002, "amount": 50000, "currency": "INR", "gateway": "razorpay"}'
```

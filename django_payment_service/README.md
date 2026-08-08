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
│   ├── urls.py             # Local routes for the payments app
│   └── tests.py            # Automated mock API tests
│
├── requirements.txt        # Dependencies (Django, Stripe, Razorpay, python-dotenv)
├── .env                    # Key configurations (Stripe keys, Razorpay keys)
├── .env.template           # Template for environment configuration
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
Copy `.env.template` to `.env` and configure your API credentials:
```bash
cp .env.template .env
```
Open `.env` and fill in the values:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True

STRIPE_API_KEY=sk_test_...your_stripe_key_here
STRIPE_WEBHOOK_SECRET=whsec_...your_stripe_webhook_secret_here

RAZORPAY_KEY_ID=rzp_test_...your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=...your_razorpay_key_secret_here
```

### 5. Initialize Database & Run Server
Run database migrations and start the development server:
```bash
python manage.py migrate
python manage.py runserver
```
The server will start on `http://127.0.0.1:8000/`.

### 6. Run Automated Tests
```bash
python manage.py test
```

---

## API Reference

### 1. Create Payment Link
Generates a checkout/payment link dynamically using the specified payment gateway.

* **URL**: `/api/payments/create-link/`
* **Method**: `POST`
* **Headers**: `Content-Type: application/json`
* **Payload Fields**:
  - `order_id` (Integer, Required): Unique ID of the order.
  - `amount` (Integer, Required): The total amount in the smallest currency subunit (e.g. cents for USD, paise for INR).
  - `currency` (String, Optional): 3-letter ISO code. Defaults to `"USD"`.
  - `gateway` (String, Required): Selected provider (must be `"stripe"` or `"razorpay"`).

#### Success Response (201 Created)
* **Body**:
  ```json
  {
    "success": true,
    "gateway": "stripe",
    "order_id": 2026,
    "amount": 1500,
    "currency": "USD",
    "payment_link": "https://checkout.stripe.com/c/pay/cs_test_..."
  }
  ```

#### Error Response: Missing Fields (400 Bad Request)
* **Body**:
  ```json
  {
    "error": "amount is required (in cents/paise)"
  }
  ```

#### Error Response: Unsupported Gateway (400 Bad Request)
* **Body**:
  ```json
  {
    "error": "Unsupported payment gateway: 'paypal'. Supported gateways: 'stripe', 'razorpay'."
  }
  ```

#### Error Response: Gateway/Credentials Authentication Failure (500 Internal Server Error)
* **Body**:
  ```json
  {
    "error": "Stripe Payment Session creation failed: Invalid API Key provided: sk_test_..."
  }
  ```

---

### 2. Payment Success Redirect Page
Stripe and Razorpay sessions redirect customers to this endpoint upon successful payment completion.

* **URL**: `/api/payments/success/`
* **Method**: `GET`
* **Query Parameters**:
  - `session_id` (String, Optional): The Stripe checkout session ID.
* **Response (200 OK - HTML)**:
  ```html
  <html>
    <body>
      <h2 style="color: green;">Payment Successful!</h2>
      <p>Thank you for your purchase. Session ID: cs_test_12345</p>
    </body>
  </html>
  ```

---

### 3. Payment Cancel Redirect Page
Stripe sessions redirect customers to this endpoint if the transaction is cancelled.

* **URL**: `/api/payments/cancel/`
* **Method**: `GET`
* **Response (200 OK - HTML)**:
  ```html
  <html>
    <body>
      <h2 style="color: red;">Payment Cancelled</h2>
      <p>The transaction was cancelled by the user.</p>
    </body>
  </html>
  ```

---

### 4. Payment Callback / Webhook Endpoint
Listens for callback status payload events from Razorpay or Stripe.

* **URL**: `/api/payments/callback/`
* **Method**: `GET` / `POST`
* **Response (200 OK - HTML)**:
  ```html
  <html>
    <body>
      <h2 style="color: blue;">Payment Callback</h2>
      <p>Callback webhook trigger processed successfully.</p>
    </body>
  </html>
  ```

---

## Verification & Manual Testing

You can use `curl` to test the creation endpoint from your command line:

### Testing Stripe Link Generation
```bash
curl -X POST http://127.0.0.1:8000/api/payments/create-link/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1001, "amount": 1000, "currency": "USD", "gateway": "stripe"}'
```

### Testing Razorpay Link Generation
```bash
curl -X POST http://127.0.0.1:8000/api/payments/create-link/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1002, "amount": 50000, "currency": "INR", "gateway": "razorpay"}'
```

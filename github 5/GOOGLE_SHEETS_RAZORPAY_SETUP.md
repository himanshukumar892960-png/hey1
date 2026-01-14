# 🚀 Complete Google Sheets + Razorpay Integration Guide

## 📋 Overview

This guide will help you set up a complete data tracking system for your website using Google Sheets and Razorpay payment integration.

## 🎯 What This System Tracks

### ✅ **7 Comprehensive Sheets**

1. **Pro Users** - Main tracking sheet with all payment details
2. **User Registrations** - All user sign-ups (Free & Pro)
3. **Promo Code History** - Track all promo code redemptions
4. **Payment History** - Complete transaction log
5. **Failed Payments** - Debug payment issues
6. **Account Upgrades** - Track FREE → PRO conversions
7. **Revenue Summary** - Daily revenue analytics

### 📊 **Data Captured**

- ✅ User Information (Email, Name, Phone)
- ✅ Payment Method (Razorpay, Promo Code)
- ✅ Payment Details (Card, UPI, Wallet, NetBanking)
- ✅ Transaction IDs (Razorpay Order ID, Payment ID)
- ✅ Amount & Currency
- ✅ Promo Codes Used
- ✅ Activation & Expiry Dates
- ✅ Days Remaining & Status
- ✅ IP Address & User Agent
- ✅ Success/Failed Status
- ✅ Error Messages

---

## 🔧 Step 1: Deploy Google Apps Script

### 1.1 Create/Open Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet or open your existing one
3. Name it: **"GlobleXGPT Pro Plan Tracker"**

### 1.2 Open Apps Script Editor

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. Delete any existing code in `Code.gs`
3. Copy the **ENTIRE** contents of `google_apps_script_enhanced.js`
4. Paste it into `Code.gs`
5. Click **Save** (💾 icon or Ctrl+S)
6. Name the project: **"GlobleXGPT Manager v3.0"**

### 1.3 Run Initial Setup

1. In the Apps Script editor, find the function dropdown (top toolbar)
2. Select **`setupSheets`** from the dropdown
3. Click **Run** (▶️ icon)
4. **IMPORTANT**: You'll see an authorization prompt:
   - Click **Review Permissions**
   - Choose your Google account
   - Click **Advanced** → **Go to GlobleXGPT Manager (unsafe)**
   - Click **Allow**
5. Wait for execution to complete (check the Execution log)
6. Go back to your Google Sheet - you should now see **7 new sheets** created!

### 1.4 Deploy as Web App

1. In Apps Script editor, click **Deploy** → **New deployment**
2. Click the gear icon (⚙️) next to "Select type"
3. Select **Web app**
4. Configure deployment:
   - **Description**: `GlobleXGPT Pro Plan Manager v3.0`
   - **Execute as**: `Me (your-email@gmail.com)`
   - **Who has access**: **Anyone** ⚠️ **CRITICAL - Must be "Anyone"!**
5. Click **Deploy**
6. **Copy the Web App URL** - it looks like:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```
7. **SAVE THIS URL** - you'll need it in the next step!

### 1.5 Set Up Daily Auto-Update (Optional but Recommended)

1. In Apps Script editor, select **`createDailyTrigger`** from the function dropdown
2. Click **Run** (▶️)
3. This creates automatic daily updates at 2 AM and 3 AM

---

## 🔑 Step 2: Update Your .env File

Open your `.env` file and update the Google Sheets URL:

```env
# Google Sheets Integration
GOOGLE_SHEETS_SCRIPT_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
```

**Replace** `YOUR_DEPLOYMENT_ID` with the actual URL you copied in Step 1.4!

---

## 💳 Step 3: Verify Razorpay Configuration

Your Razorpay credentials are already in `.env`:

```env
# Razorpay Payment Gateway
RAZORPAY_KEY_ID=rzp_test_S3FCJT8AWieK6j
RAZORPAY_KEY_SECRET=yf2pqm3eRpg20bl2w5LtUSOp
```

### ⚠️ **IMPORTANT**: Test vs Live Mode

- **Test Mode** (current): Keys start with `rzp_test_`
  - Use test card: `4111 1111 1111 1111`
  - Any future date, any CVV
  - No real money charged

- **Live Mode** (production): Keys start with `rzp_live_`
  - Real payments
  - Real money charged
  - Get from [Razorpay Dashboard](https://dashboard.razorpay.com/app/keys)

---

## 🧪 Step 4: Test the Integration

### 4.1 Test User Registration

1. Start your Flask app:
   ```bash
   python app.py
   ```

2. Open your website and sign up with a new account

3. Check the **"User Registrations"** sheet - you should see the new user!

### 4.2 Test Promo Code Upgrade

1. Log in to your website
2. Click on **Pro Plan** button
3. Enter promo code: `HIMANSHU2026` (or your current active code)
4. Click **Apply**

5. Check these sheets:
   - ✅ **Pro Users** - New entry with promo code
   - ✅ **Promo Code History** - Code usage logged
   - ✅ **Payment History** - Promo upgrade recorded
   - ✅ **Account Upgrades** - FREE → PRO conversion

### 4.3 Test Razorpay Payment

1. Log in with a FREE account
2. Click **Upgrade to Pro**
3. Click **Pay with Razorpay**
4. Use test card details:
   - **Card Number**: `4111 1111 1111 1111`
   - **Expiry**: Any future date (e.g., `12/25`)
   - **CVV**: Any 3 digits (e.g., `123`)
   - **Name**: Your name
5. Complete payment

6. Check these sheets:
   - ✅ **Pro Users** - New entry with Razorpay details
   - ✅ **Payment History** - Transaction logged with Order ID & Payment ID
   - ✅ **Account Upgrades** - Upgrade recorded

### 4.4 Test Failed Payment

1. In Razorpay test mode, use this card to simulate failure:
   - **Card Number**: `4000 0000 0000 0002`
2. Complete the payment flow

3. Check these sheets:
   - ✅ **Failed Payments** - Failed transaction logged
   - ✅ **Payment History** - Status marked as "FAILED"

---

## 📊 Step 5: Understanding Your Data

### Sheet 1: Pro Users
**Purpose**: Master list of all PRO users

**Key Columns**:
- Email, Name, Phone
- Payment Method & Details
- Amount, Transaction IDs
- Razorpay Order ID & Payment ID
- Promo Code (if used)
- Activation Date, Expiry Date
- Days Remaining, Status (ACTIVE/EXPIRED)
- IP Address, User Agent

**Color Coding**:
- 🟢 Green: Active (>7 days remaining)
- 🟡 Yellow: Expiring soon (≤7 days)
- 🔴 Red: Expired

### Sheet 2: User Registrations
**Purpose**: Track all user sign-ups

**Tracks**:
- Registration timestamp
- Email, Name
- Registration method (Email, Google, GitHub)
- Initial plan type (FREE/PRO)

### Sheet 3: Promo Code History
**Purpose**: Monitor promo code usage

**Tracks**:
- Which codes are used
- Who used them
- When they were used
- Activation & expiry dates

### Sheet 4: Payment History
**Purpose**: Complete transaction log

**Tracks**:
- All payment attempts (success & failed)
- Payment methods used
- Transaction amounts
- Razorpay IDs
- Error messages for failed payments

### Sheet 5: Failed Payments
**Purpose**: Debug payment issues

**Tracks**:
- Failed payment attempts
- Error messages
- User details for follow-up

### Sheet 6: Account Upgrades
**Purpose**: Track conversions

**Tracks**:
- FREE → PRO upgrades
- Upgrade method (Razorpay/Promo)
- Validity period

### Sheet 7: Revenue Summary
**Purpose**: Daily analytics

**Auto-updates daily** with:
- Total revenue
- Number of Razorpay payments
- Number of promo upgrades
- Total/Active/Expired users

---

## 🔄 Step 6: API Endpoints

Your Google Apps Script provides these endpoints:

### GET Requests

```bash
# Get active PRO users
GET https://script.google.com/macros/s/YOUR_ID/exec?action=active

# Get all PRO users (active + expired)
GET https://script.google.com/macros/s/YOUR_ID/exec?action=all

# Get expired PRO users
GET https://script.google.com/macros/s/YOUR_ID/exec?action=expired

# Get revenue statistics
GET https://script.google.com/macros/s/YOUR_ID/exec?action=revenue
```

### POST Requests

```bash
# Register new user
POST https://script.google.com/macros/s/YOUR_ID/exec
Content-Type: application/json

{
  "action": "register",
  "email": "user@example.com",
  "name": "John Doe",
  "registration_method": "Email",
  "plan_type": "FREE",
  "ip_address": "192.168.1.1"
}

# Record PRO upgrade (Razorpay or Promo)
POST https://script.google.com/macros/s/YOUR_ID/exec
Content-Type: application/json

{
  "action": "pro_upgrade",
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+91 9876543210",
  "payment_method": "Razorpay",
  "payment_details": "Credit Card",
  "amount": "499",
  "transaction_id": "txn_123456",
  "razorpay_order_id": "order_123456",
  "razorpay_payment_id": "pay_123456",
  "promo_code": "N/A",
  "plan_type": "PRO",
  "ip_address": "192.168.1.1"
}

# Log failed payment
POST https://script.google.com/macros/s/YOUR_ID/exec
Content-Type: application/json

{
  "action": "payment_failed",
  "email": "user@example.com",
  "name": "John Doe",
  "payment_method": "Razorpay",
  "amount": "499",
  "razorpay_order_id": "order_123456",
  "error_message": "Payment declined by bank",
  "ip_address": "192.168.1.1"
}
```

---

## 🛠️ Step 7: Backend Integration

Your `app.py` should already have the integration code. Here's what it does:

### On User Registration
```python
# Sends user data to "User Registrations" sheet
send_to_google_sheets({
    "action": "register",
    "email": user_email,
    "name": user_name,
    "registration_method": "Email",
    "plan_type": "FREE"
})
```

### On Promo Code Success
```python
# Sends to "Pro Users", "Promo Code History", "Payment History", "Account Upgrades"
send_to_google_sheets({
    "action": "pro_upgrade",
    "email": user_email,
    "name": user_name,
    "payment_method": "Promo Code",
    "promo_code": promo_code,
    "amount": "0",
    "plan_type": "PRO"
})
```

### On Razorpay Success
```python
# Sends complete payment details to all relevant sheets
send_to_google_sheets({
    "action": "payment_success",
    "email": user_email,
    "name": user_name,
    "phone": user_phone,
    "payment_method": "Razorpay",
    "payment_details": payment_method,  # Card/UPI/Wallet/NetBanking
    "amount": "499",
    "transaction_id": transaction_id,
    "razorpay_order_id": order_id,
    "razorpay_payment_id": payment_id,
    "plan_type": "PRO"
})
```

### On Payment Failure
```python
# Logs failed payment for debugging
send_to_google_sheets({
    "action": "payment_failed",
    "email": user_email,
    "name": user_name,
    "payment_method": "Razorpay",
    "amount": "499",
    "razorpay_order_id": order_id,
    "error_message": error_description
})
```

---

## 🎨 Step 8: Frontend Integration

Your frontend should capture:

### Payment Method Details

When Razorpay payment succeeds, capture the payment method:

```javascript
razorpay.on('payment.success', function(response) {
    // Extract payment method from response
    const paymentMethod = response.razorpay_payment_method || 'Unknown';
    
    // Map to readable format
    const methodMap = {
        'card': 'Credit/Debit Card',
        'upi': 'UPI',
        'wallet': 'Wallet',
        'netbanking': 'Net Banking'
    };
    
    const paymentDetails = methodMap[paymentMethod] || paymentMethod;
    
    // Send to backend
    fetch('/verify-payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            payment_details: paymentDetails
        })
    });
});
```

---

## 📈 Step 9: Monitoring & Analytics

### Daily Auto-Updates

The system automatically updates every day:

- **2:00 AM**: Updates all user statuses (Days Remaining, ACTIVE/EXPIRED)
- **3:00 AM**: Generates daily revenue summary

### Manual Refresh

To manually update all statuses:

1. Open Apps Script editor
2. Select `updateAllUserStatus` function
3. Click **Run**

### View Revenue Stats

Access revenue statistics via API:

```bash
curl "https://script.google.com/macros/s/YOUR_ID/exec?action=revenue"
```

Response:
```json
{
  "total_revenue": 4990,
  "razorpay_payments": 8,
  "promo_upgrades": 2,
  "total_pro_users": 10,
  "active_users": 8,
  "expired_users": 2
}
```

---

## 🔒 Security Best Practices

### 1. Google Apps Script Security

✅ **DO**:
- Set "Execute as" to "Me"
- Set "Who has access" to "Anyone" (required for API access)
- Keep your script URL private
- Use HTTPS only

❌ **DON'T**:
- Share your script URL publicly
- Hardcode sensitive data in the script
- Allow script editing by others

### 2. Razorpay Security

✅ **DO**:
- Always verify payment signatures on backend
- Use environment variables for keys
- Never expose secret key to frontend
- Use test mode for development
- Switch to live mode only in production

❌ **DON'T**:
- Trust frontend payment data without verification
- Hardcode API keys in code
- Commit keys to version control
- Use test keys in production

### 3. Data Privacy

✅ **DO**:
- Limit Google Sheet access to authorized users only
- Use IP logging for security audits
- Regularly review access logs
- Comply with data protection regulations

---

## 🐛 Troubleshooting

### Issue: "Sheet not found" error

**Solution**:
1. Open Apps Script editor
2. Run `setupSheets()` function manually
3. Verify all 7 sheets are created

### Issue: Data not appearing in sheets

**Solution**:
1. Check your `.env` file has correct `GOOGLE_SHEETS_SCRIPT_URL`
2. Verify script deployment is set to "Anyone" access
3. Check Apps Script execution logs for errors
4. Test the endpoint directly with curl/Postman

### Issue: Payment succeeds but not logged

**Solution**:
1. Check backend logs for errors
2. Verify `send_to_google_sheets()` function is called
3. Check if `action` parameter is correct
4. Test with a simple POST request to the script URL

### Issue: Razorpay payment fails

**Solution**:
1. Verify Razorpay keys in `.env`
2. Check if using correct test/live mode
3. Review Razorpay dashboard for error details
4. Check "Failed Payments" sheet for error messages

---

## 📞 Support

### Razorpay Support
- Dashboard: https://dashboard.razorpay.com
- Docs: https://razorpay.com/docs
- Test Cards: https://razorpay.com/docs/payments/payments/test-card-details

### Google Apps Script Support
- Docs: https://developers.google.com/apps-script
- Reference: https://developers.google.com/apps-script/reference

---

## ✅ Checklist

Before going live, ensure:

- [ ] Google Apps Script deployed successfully
- [ ] All 7 sheets created and visible
- [ ] `GOOGLE_SHEETS_SCRIPT_URL` updated in `.env`
- [ ] Razorpay keys configured (test mode for testing)
- [ ] Test user registration works
- [ ] Test promo code upgrade works
- [ ] Test Razorpay payment works (test mode)
- [ ] Test failed payment logging works
- [ ] Daily triggers created
- [ ] All sheets showing correct data
- [ ] Revenue summary updating correctly
- [ ] Frontend captures payment method details
- [ ] Backend verifies Razorpay signatures
- [ ] Switch to Razorpay live mode for production
- [ ] Monitor first few real transactions

---

## 🎉 You're All Set!

Your complete Google Sheets + Razorpay integration is now live! 

Every user action will be automatically tracked:
- ✅ User registrations
- ✅ Promo code redemptions  
- ✅ Razorpay payments
- ✅ Failed transactions
- ✅ Account upgrades
- ✅ Daily revenue analytics

All data is securely stored in your Google Sheet with automatic daily updates!

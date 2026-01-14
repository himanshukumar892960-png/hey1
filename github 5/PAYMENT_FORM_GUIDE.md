# Payment Form Setup Guide

## Features Added

### 1. **Enhanced Pro Plan Modal**
- ✅ Full Name input field
- ✅ Phone Number input field  
- ✅ Email ID input field
- ✅ Payment Screenshot upload with preview
- ✅ Submit button to send payment details

### 2. **Email Notification System**
- ✅ Sends formatted HTML email to: **heyhkhimanshu@gmail.com**
- ✅ Includes all customer details (name, email, phone, amount)
- ✅ Attaches payment screenshot
- ✅ Professional email template with styling

### 3. **Data Storage**
- ✅ Logs payment details in server logs
- ✅ Stores in Supabase database (if configured)
- ✅ Timestamp tracking

## Setup Instructions

### Step 1: Configure SMTP Email (Required for Email Sending)

Add these lines to your `.env` file:

```env
# SMTP Configuration for Payment Notifications
SMTP_EMAIL=your-gmail@gmail.com
SMTP_PASSWORD=your-app-password
```

#### How to Get Gmail App Password:

1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", enable "2-Step Verification" (if not already enabled)
4. After enabling 2FA, go back to Security
5. Under "Signing in to Google", click on "App passwords"
6. Select "Mail" and "Other (Custom name)"
7. Enter "GlobleXGPT" as the name
8. Click "Generate"
9. Copy the 16-character password
10. Paste it as `SMTP_PASSWORD` in your `.env` file

### Step 2: Create Database Table (Optional)

If you want to store payment submissions in Supabase, run this SQL in your Supabase SQL Editor:

```sql
CREATE TABLE payment_submissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    amount TEXT NOT NULL,
    timestamp TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add index for faster queries
CREATE INDEX idx_payment_email ON payment_submissions(email);
CREATE INDEX idx_payment_created ON payment_submissions(created_at DESC);
```

### Step 3: Restart the Server

After adding SMTP credentials to `.env`, restart your Flask server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
python app.py
```

## How It Works

### User Flow:
1. User clicks "Upgrade to Pro" button
2. Fills in:
   - Full Name
   - Phone Number
   - Email Address
3. Scans QR code and makes payment
4. Uploads payment screenshot
5. Clicks "Submit Payment Details"

### Backend Process:
1. Validates all input fields
2. Sends email to **heyhkhimanshu@gmail.com** with:
   - Customer name, email, phone
   - Payment amount (₹90)
   - Payment screenshot (attached)
   - Timestamp
3. Logs payment details in server logs
4. Stores in database (if Supabase configured)
5. Returns success message to user

## Email Template Preview

The email sent to heyhkhimanshu@gmail.com will look like this:

```
Subject: 🎉 New Pro Plan Payment - [Customer Name]

💰 New Pro Plan Payment Received!

Customer Details
─────────────────
Name:      [Customer Name]
Email:     [customer@email.com]
Phone:     [+91 XXXXX XXXXX]
Amount:    ₹90
Submitted: [2026-01-07 10:45:30]

📸 Payment Screenshot: Attached to this email

─────────────────
This is an automated notification from GlobleXGPT Pro Plan System
```

## Testing Without SMTP

If you don't configure SMTP credentials, the system will still work:
- ✅ Payment details will be logged in server console
- ✅ Data will be stored in database (if Supabase configured)
- ⚠️ Email will NOT be sent (but no error shown to user)

## Security Notes

- Payment screenshots are sent as email attachments
- All data is validated before processing
- Email and phone number formats are checked
- SMTP password should be an "App Password", not your main Gmail password
- Never commit `.env` file to version control

## Troubleshooting

### Email Not Sending?
1. Check if SMTP_EMAIL and SMTP_PASSWORD are in `.env`
2. Verify you're using an App Password, not regular password
3. Check server logs for SMTP errors
4. Ensure 2-Factor Authentication is enabled on Gmail

### Form Not Submitting?
1. Check browser console for JavaScript errors
2. Verify all fields are filled
3. Ensure payment screenshot is uploaded
4. Check network tab for API response

### Database Errors?
1. Verify Supabase credentials in `.env`
2. Ensure `payment_submissions` table exists
3. Check table permissions

## Files Modified

1. **templates/index.html** - Added form fields and screenshot upload
2. **static/js/main.js** - Added form validation and submission logic
3. **app.py** - Added `/submit_payment` endpoint
4. **FIXES_APPLIED.md** - Previous fixes documentation

## Support

For issues or questions, contact: heyhkhimanshu@gmail.com

# 🚀 GlobleXGPT Pro Plan Management - Google Apps Script Deployment Guide

## 📋 Overview

This enhanced Google Apps Script tracks:
- ✅ **All promo code usage** with detailed history
- ✅ **Payment methods** (Razorpay, Promo Codes)
- ✅ **Automatic 30-day validity** calculation
- ✅ **Account upgrade tracking** from FREE to PRO
- ✅ **Real-time expiry validation**
- ✅ **Comprehensive user analytics**

---

## 🎯 Step-by-Step Deployment

### Step 1: Create/Open Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet or open your existing one
3. Name it: **"GlobleXGPT Pro Plan Manager"**

### Step 2: Open Apps Script Editor

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. Delete any existing code in the editor
3. Copy the entire content from `google_apps_script.js`
4. Paste it into the Apps Script editor
5. **Save** the project (Ctrl+S or Cmd+S)
6. Name the project: **"GlobleXGPT Backend v2.0"**

### Step 3: Run Initial Setup

1. In the Apps Script editor, find the function dropdown (top toolbar)
2. Select **`setupSheets`** from the dropdown
3. Click the **Run** button (▶️)
4. **IMPORTANT**: You'll be asked to authorize the script:
   - Click **Review Permissions**
   - Choose your Google account
   - Click **Advanced** → **Go to [Project Name] (unsafe)**
   - Click **Allow**
5. Wait for execution to complete (check the logs)

### Step 4: Verify Sheet Creation

Go back to your Google Sheet. You should now see **4 tabs**:

1. **Pro Users** - Main tracking sheet (Blue header)
2. **Promo Code History** - All promo code redemptions (Green header)
3. **Payment History** - All payment transactions (Yellow header)
4. **Account Upgrades** - Upgrade tracking (Red header)

### Step 5: Deploy as Web App

1. In Apps Script editor, click **Deploy** → **New deployment**
2. Click the gear icon ⚙️ next to "Select type"
3. Choose **Web app**
4. Configure deployment:
   - **Description**: `GlobleXGPT Pro Plan Manager v2.0`
   - **Execute as**: `Me (your-email@gmail.com)`
   - **Who has access**: `Anyone` ⚠️ **CRITICAL - Must be "Anyone"!**
5. Click **Deploy**
6. **Copy the Web app URL** (it will look like):
   ```
   https://script.google.com/macros/s/XXXXXXXXXX.../exec
   ```

### Step 6: Update Your .env File

1. Open your `.env` file
2. Update the `GOOGLE_SHEETS_SCRIPT_URL` with your new Web app URL:
   ```env
   GOOGLE_SHEETS_SCRIPT_URL=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec
   ```
3. Save the `.env` file

### Step 7: (Optional) Enable Auto-Update

To automatically update user status daily:

1. In Apps Script editor, select **`createDailyTrigger`** from the function dropdown
2. Click **Run** (▶️)
3. This will create a daily trigger that runs at 2 AM to:
   - Update "Days Remaining" for all users
   - Update "Status" (ACTIVE/EXPIRED)
   - Color-code rows based on status

---

## 📊 Sheet Structure

### 1️⃣ Pro Users Sheet
| Column | Field | Description |
|--------|-------|-------------|
| A | Timestamp | When user was added/updated |
| B | Email | User's email (unique identifier) |
| C | Name | User's full name |
| D | Phone | Contact number |
| E | Payment Method | Razorpay, Promo Code, etc. |
| F | Amount | Payment amount (0 for promo) |
| G | Promo Code | Code used (if applicable) |
| H | Plan Type | PRO, PRO+, etc. |
| I | Activation Date | When plan started |
| J | Expiry Date | When plan expires (30 days) |
| K | Days Remaining | Auto-calculated |
| L | Status | ACTIVE or EXPIRED |
| M | IP Address | User's IP |

### 2️⃣ Promo Code History
Tracks every promo code redemption with activation and expiry dates.

### 3️⃣ Payment History
Logs all payment transactions including Razorpay payments.

### 4️⃣ Account Upgrades
Records when users upgrade from FREE to PRO.

---

## 🔌 API Endpoints

### POST Request (Add/Update User)
**URL**: Your Web app URL

**Method**: POST

**Payload Example**:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "1234567890",
  "payment_method": "Promo Code",
  "amount": "0",
  "promo_code": "WELCOME2024",
  "plan_type": "PRO",
  "activation_date": "2026-01-12",
  "ip_address": "192.168.1.1"
}
```

**Response**:
```json
{
  "result": "success",
  "message": "Pro plan activated successfully",
  "expiry_date": "2026-02-11",
  "days_remaining": 30,
  "status": "ACTIVE"
}
```

### GET Request (Retrieve Users)

**Get Active Users** (default):
```
https://your-script-url/exec
```

**Get All Users**:
```
https://your-script-url/exec?action=all
```

**Get Expired Users**:
```
https://your-script-url/exec?action=expired
```

**Response Example**:
```json
[
  {
    "email": "user@example.com",
    "name": "John Doe",
    "plan_type": "PRO",
    "expiry_date": "2026-02-11",
    "days_remaining": 30,
    "status": "ACTIVE"
  }
]
```

---

## 🎨 Color Coding (Auto-Applied)

- 🟢 **Green** (`#e8f5e9`) - Active with 8+ days remaining
- 🟡 **Yellow** (`#fff9c4`) - Active with ≤7 days remaining (expiring soon)
- 🔴 **Red** (`#ffebee`) - Expired

---

## 🔧 Maintenance Functions

### Update All User Status Manually
Run this anytime to refresh all user statuses:
```javascript
updateAllUserStatus()
```

### View Logs
In Apps Script editor: **View** → **Logs** (or Ctrl+Enter)

---

## 🛠️ Troubleshooting

### Issue: "Sheet not found" error
**Solution**: Run `setupSheets()` function manually

### Issue: POST requests failing
**Solution**: Verify deployment settings - "Who has access" must be "Anyone"

### Issue: Data not updating
**Solution**: 
1. Check the execution logs in Apps Script
2. Verify the Web app URL is correct in `.env`
3. Redeploy the script (Deploy → Manage deployments → Edit → New version)

### Issue: Trigger not working
**Solution**: 
1. Go to Apps Script → Triggers (clock icon)
2. Delete existing triggers
3. Run `createDailyTrigger()` again

---

## 📈 Usage Statistics

To view analytics:
1. Open your Google Sheet
2. Navigate between the 4 tabs
3. Use Google Sheets' built-in charts and pivot tables for visualization

---

## 🔐 Security Notes

- ✅ Script runs under your Google account
- ✅ Only you can edit the script
- ✅ Web app is accessible to anyone (required for backend integration)
- ✅ No sensitive data should be stored in the script itself
- ✅ All API keys remain in your `.env` file

---

## 📞 Support

If you encounter issues:
1. Check the Apps Script execution logs
2. Verify all deployment steps were followed
3. Ensure `.env` file has the correct Web app URL
4. Test the endpoint using Postman or curl

---

## ✅ Deployment Checklist

- [ ] Created/opened Google Sheet
- [ ] Opened Apps Script editor
- [ ] Pasted script code
- [ ] Saved project
- [ ] Ran `setupSheets()` function
- [ ] Authorized script permissions
- [ ] Verified 4 sheets were created
- [ ] Deployed as Web app
- [ ] Set "Who has access" to "Anyone"
- [ ] Copied Web app URL
- [ ] Updated `.env` file
- [ ] (Optional) Ran `createDailyTrigger()`
- [ ] Tested POST request
- [ ] Tested GET request

---

**🎉 Congratulations! Your Pro Plan Management System is now live!**

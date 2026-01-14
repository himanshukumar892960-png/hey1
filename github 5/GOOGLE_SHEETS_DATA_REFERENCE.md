# 📊 Google Sheets Data Structure - Quick Reference

## 🎯 Required Data Fields for POST Requests

When sending data from your Python backend to Google Sheets, include these fields:

```python
data = {
    # ═══════════════════════════════════════════════════════════════
    # REQUIRED FIELDS
    # ═══════════════════════════════════════════════════════════════
    "email": "user@example.com",           # User's email (unique ID)
    "name": "John Doe",                     # User's full name
    
    # ═══════════════════════════════════════════════════════════════
    # PAYMENT/PROMO FIELDS
    # ═══════════════════════════════════════════════════════════════
    "payment_method": "Promo Code",         # Options: "Razorpay", "Promo Code", "Manual"
    "amount": "0",                          # Payment amount (0 for promo codes)
    "promo_code": "WELCOME2024",            # Promo code used (or "N/A")
    "transaction_id": "txn_123456",         # Razorpay transaction ID (optional)
    
    # ═══════════════════════════════════════════════════════════════
    # PLAN DETAILS
    # ═══════════════════════════════════════════════════════════════
    "plan_type": "PRO",                     # Plan name (PRO, PRO+, etc.)
    "activation_date": "2026-01-12",        # YYYY-MM-DD format
    # "expiry_date" is auto-calculated as activation_date + 30 days
    
    # ═══════════════════════════════════════════════════════════════
    # OPTIONAL FIELDS
    # ═══════════════════════════════════════════════════════════════
    "phone": "1234567890",                  # User's phone number
    "ip_address": "192.168.1.1",            # User's IP address
    "timestamp": "2026-01-12T11:30:00Z"     # Auto-generated if not provided
}
```

---

## 🔄 Example Use Cases

### 1️⃣ User Upgrades via Promo Code

```python
import requests
import json
from datetime import datetime

# Your Google Apps Script Web App URL
SCRIPT_URL = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"

# Promo code upgrade data
promo_data = {
    "email": "user@example.com",
    "name": "Jane Smith",
    "phone": "9876543210",
    "payment_method": "Promo Code",
    "amount": "0",
    "promo_code": "NEWYEAR2026",
    "plan_type": "PRO",
    "activation_date": datetime.now().strftime("%Y-%m-%d"),
    "ip_address": "203.0.113.42"
}

# Send to Google Sheets
response = requests.post(
    SCRIPT_URL,
    data=json.dumps(promo_data),
    headers={"Content-Type": "application/json"}
)

print(response.json())
# Output: {
#   "result": "success",
#   "message": "Pro plan activated successfully",
#   "expiry_date": "2026-02-11",
#   "days_remaining": 30,
#   "status": "ACTIVE"
# }
```

### 2️⃣ User Pays via Razorpay

```python
# Razorpay payment data
payment_data = {
    "email": "premium@example.com",
    "name": "John Premium",
    "phone": "5551234567",
    "payment_method": "Razorpay",
    "amount": "499",
    "promo_code": "N/A",
    "plan_type": "PRO",
    "activation_date": "2026-01-12",
    "transaction_id": "pay_123456789",
    "ip_address": "198.51.100.10"
}

response = requests.post(SCRIPT_URL, data=json.dumps(payment_data))
print(response.json())
```

### 3️⃣ Retrieve Active PRO Users

```python
# Get only active users (default)
response = requests.get(SCRIPT_URL)
active_users = response.json()

for user in active_users:
    print(f"{user['name']} - {user['email']} - {user['days_remaining']} days left")
```

### 4️⃣ Retrieve All Users (Including Expired)

```python
# Get all users
response = requests.get(f"{SCRIPT_URL}?action=all")
all_users = response.json()

print(f"Total users: {len(all_users)}")
```

### 5️⃣ Check Expired Users

```python
# Get only expired users
response = requests.get(f"{SCRIPT_URL}?action=expired")
expired_users = response.json()

print(f"Expired users: {len(expired_users)}")
for user in expired_users:
    print(f"{user['name']} - Expired on {user['expiry_date']}")
```

---

## 📋 Sheet Columns Explained

### Pro Users Sheet (Main)

| Column | Field | Auto-Calculated? | Description |
|--------|-------|------------------|-------------|
| A | Timestamp | ✅ Yes | When record was created/updated |
| B | Email | ❌ No | User's unique email |
| C | Name | ❌ No | User's display name |
| D | Phone | ❌ No | Contact number |
| E | Payment Method | ❌ No | How they got PRO |
| F | Amount | ❌ No | Payment amount |
| G | Promo Code | ❌ No | Code used (if any) |
| H | Plan Type | ❌ No | PRO, PRO+, etc. |
| I | Activation Date | ❌ No | When plan started |
| J | Expiry Date | ✅ Yes | Activation + 30 days |
| K | Days Remaining | ✅ Yes | Days until expiry |
| L | Status | ✅ Yes | ACTIVE or EXPIRED |
| M | IP Address | ❌ No | User's IP |

---

## 🎨 Status Color Coding

The script automatically applies colors based on status:

```javascript
// Green - Active with plenty of time
if (status === "ACTIVE" && daysRemaining > 7) {
    backgroundColor = "#e8f5e9"; // Light green
}

// Yellow - Expiring soon (warning)
if (status === "ACTIVE" && daysRemaining <= 7) {
    backgroundColor = "#fff9c4"; // Light yellow
}

// Red - Expired
if (status === "EXPIRED") {
    backgroundColor = "#ffebee"; // Light red
}
```

---

## 🔍 Validation Rules

### Email Validation
- Must be unique per user
- If email exists, record is **updated** (not duplicated)
- If email is new, record is **appended**

### Date Format
- **Activation Date**: `YYYY-MM-DD` (e.g., `2026-01-12`)
- **Expiry Date**: Auto-calculated as `activation_date + 30 days`

### Payment Method Options
- `"Razorpay"` - Paid via Razorpay gateway
- `"Promo Code"` - Activated via promo code
- `"Manual"` - Manually added by admin
- `"Unknown"` - Default if not specified

### Promo Code Rules
- If `payment_method` contains "promo" (case-insensitive)
- AND `promo_code` is not "N/A"
- THEN entry is logged in "Promo Code History" sheet

---

## 🚀 Integration with Python Backend

### Example Flask Route

```python
from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"

@app.route('/upgrade-to-pro', methods=['POST'])
def upgrade_to_pro():
    user_data = request.json
    
    # Prepare data for Google Sheets
    sheet_data = {
        "email": user_data.get('email'),
        "name": user_data.get('name'),
        "phone": user_data.get('phone', ''),
        "payment_method": user_data.get('payment_method', 'Unknown'),
        "amount": user_data.get('amount', '0'),
        "promo_code": user_data.get('promo_code', 'N/A'),
        "plan_type": "PRO",
        "activation_date": datetime.now().strftime("%Y-%m-%d"),
        "ip_address": request.remote_addr,
        "transaction_id": user_data.get('transaction_id', '')
    }
    
    # Send to Google Sheets
    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            data=json.dumps(sheet_data),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        result = response.json()
        
        if result.get('result') == 'success':
            return jsonify({
                "success": True,
                "message": "PRO plan activated!",
                "expiry_date": result.get('expiry_date'),
                "days_remaining": result.get('days_remaining')
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 📊 Data Flow Diagram

```
┌─────────────────┐
│  User Action    │
│  (Promo/Pay)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Python Backend  │
│   (app.py)      │
└────────┬────────┘
         │ POST Request
         │ (JSON Data)
         ▼
┌─────────────────────────────────────┐
│  Google Apps Script (Web App)       │
│  ┌─────────────────────────────┐   │
│  │ 1. Validate Data            │   │
│  │ 2. Calculate Expiry (30d)   │   │
│  │ 3. Update Pro Users Sheet   │   │
│  │ 4. Log Promo Code (if used) │   │
│  │ 5. Log Payment History      │   │
│  │ 6. Log Account Upgrade      │   │
│  └─────────────────────────────┘   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Google Sheets (4 Tabs)             │
│  • Pro Users                        │
│  • Promo Code History               │
│  • Payment History                  │
│  • Account Upgrades                 │
└─────────────────────────────────────┘
```

---

## ✅ Testing Checklist

- [ ] Test promo code activation
- [ ] Test Razorpay payment
- [ ] Verify 30-day expiry calculation
- [ ] Check duplicate email handling (update vs. append)
- [ ] Verify all 4 sheets are populated correctly
- [ ] Test GET endpoint for active users
- [ ] Test GET endpoint with `?action=all`
- [ ] Test GET endpoint with `?action=expired`
- [ ] Verify color coding works
- [ ] Check daily auto-update trigger

---

**📌 Pro Tip**: Keep your Google Sheet open while testing to see real-time updates!

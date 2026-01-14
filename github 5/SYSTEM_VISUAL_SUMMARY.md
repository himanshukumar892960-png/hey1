# 📊 GlobleXGPT Pro Plan Tracking System - Visual Summary

## 🎯 System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    GLOBLE★GPT PRO PLAN SYSTEM                    │
│                  30-Day Validity • Auto-Tracking                 │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌──────────────┐
│  User Upgrades  │──────▶│ Python Backend  │──────▶│ Google Sheet │
│  (Promo/Pay)    │       │    (app.py)     │       │  (4 Sheets)  │
└─────────────────┘       └─────────────────┘       └──────────────┘
                                                            │
                                                            ▼
                                              ┌──────────────────────┐
                                              │  Auto-Calculations:  │
                                              │  • Expiry Date       │
                                              │  • Days Remaining    │
                                              │  • Status (Active)   │
                                              │  • Color Coding      │
                                              └──────────────────────┘
```

---

## 📋 Four Tracking Sheets

### 1️⃣ Pro Users (Main Dashboard)
**Purpose**: Complete overview of all PRO users

```
┌─────────────┬──────────────┬──────────┬─────────┬──────────────┐
│  Timestamp  │    Email     │   Name   │  Phone  │ Payment Type │
├─────────────┼──────────────┼──────────┼─────────┼──────────────┤
│ 2026-01-12  │ user@ex.com  │ John Doe │ 123456  │ Promo Code   │
└─────────────┴──────────────┴──────────┴─────────┴──────────────┘

┌────────┬────────────┬──────────┬──────────────┬──────────────┬────────┐
│ Amount │ Promo Code │   Plan   │ Activation   │ Expiry Date  │  Days  │
├────────┼────────────┼──────────┼──────────────┼──────────────┼────────┤
│   0    │ WELCOME24  │   PRO    │  2026-01-12  │  2026-02-11  │   30   │
└────────┴────────────┴──────────┴──────────────┴──────────────┴────────┘

┌────────┬────────────┐
│ Status │ IP Address │
├────────┼────────────┤
│ ACTIVE │ 192.168... │
└────────┴────────────┘
```

**Color Coding**:
- 🟢 Green: Active, 8+ days remaining
- 🟡 Yellow: Active, ≤7 days remaining (expiring soon!)
- 🔴 Red: Expired

---

### 2️⃣ Promo Code History
**Purpose**: Track all promo code redemptions

```
┌─────────────┬──────────────┬──────────┬────────────┬──────────────┐
│  Timestamp  │    Email     │   Name   │ Promo Code │ Activation   │
├─────────────┼──────────────┼──────────┼────────────┼──────────────┤
│ 2026-01-12  │ user1@ex.com │ Alice    │ WELCOME24  │  2026-01-12  │
│ 2026-01-12  │ user2@ex.com │ Bob      │ NEWYEAR26  │  2026-01-12  │
│ 2026-01-11  │ user3@ex.com │ Charlie  │ WELCOME24  │  2026-01-11  │
└─────────────┴──────────────┴──────────┴────────────┴──────────────┘

┌──────────────┬────────┐
│ Expiry Date  │ Status │
├──────────────┼────────┤
│  2026-02-11  │ ACTIVE │
│  2026-02-11  │ ACTIVE │
│  2026-02-10  │ ACTIVE │
└──────────────┴────────┘
```

**Use Cases**:
- See which promo codes are most popular
- Track total redemptions per code
- Identify promo code abuse

---

### 3️⃣ Payment History
**Purpose**: Log all payment transactions

```
┌─────────────┬──────────────┬──────────┬──────────────┬────────┐
│  Timestamp  │    Email     │   Name   │ Payment Type │ Amount │
├─────────────┼──────────────┼──────────┼──────────────┼────────┤
│ 2026-01-12  │ pay1@ex.com  │ David    │ Razorpay     │  499   │
│ 2026-01-12  │ pay2@ex.com  │ Emma     │ Razorpay     │  499   │
│ 2026-01-11  │ free@ex.com  │ Frank    │ Promo Code   │   0    │
└─────────────┴──────────────┴──────────┴──────────────┴────────┘

┌────────────────┬─────────┬────────────┐
│ Transaction ID │ Status  │ IP Address │
├────────────────┼─────────┼────────────┤
│ pay_123456     │ SUCCESS │ 203.0.113  │
│ pay_789012     │ SUCCESS │ 198.51.100 │
│ N/A            │ SUCCESS │ 192.168.1  │
└────────────────┴─────────┴────────────┘
```

**Use Cases**:
- Track total revenue
- Monitor payment success rate
- Reconcile Razorpay transactions

---

### 4️⃣ Account Upgrades
**Purpose**: Track user plan changes

```
┌─────────────┬──────────────┬──────────┬──────────────┬──────────┐
│  Timestamp  │    Email     │   Name   │ Previous Plan│ New Plan │
├─────────────┼──────────────┼──────────┼──────────────┼──────────┤
│ 2026-01-12  │ user@ex.com  │ Grace    │ FREE         │ PRO      │
│ 2026-01-11  │ user2@ex.com │ Henry    │ FREE         │ PRO      │
└─────────────┴──────────────┴──────────┴──────────────┴──────────┘

┌────────────────┬─────────────────┐
│ Upgrade Method │ Validity Period │
├────────────────┼─────────────────┤
│ Promo Code     │ 30 Days         │
│ Razorpay       │ 30 Days         │
└────────────────┴─────────────────┘
```

**Use Cases**:
- Track conversion rate (FREE → PRO)
- Analyze upgrade methods
- Monitor growth trends

---

## 🔄 Automatic Calculations

### 30-Day Validity System

```
┌──────────────────┐
│ Activation Date  │
│   2026-01-12     │
└────────┬─────────┘
         │
         │ + 30 Days
         ▼
┌──────────────────┐
│  Expiry Date     │
│   2026-02-11     │  ◀── Auto-calculated
└────────┬─────────┘
         │
         │ Compare with Today
         ▼
┌──────────────────┐
│ Days Remaining   │
│       30         │  ◀── Auto-updated daily
└────────┬─────────┘
         │
         │ Check Status
         ▼
┌──────────────────┐
│     Status       │
│     ACTIVE       │  ◀── ACTIVE or EXPIRED
└──────────────────┘
```

---

## 📊 Sample Data Scenarios

### Scenario 1: User Applies Promo Code

**Input (Python → Google Script)**:
```json
{
  "email": "newuser@example.com",
  "name": "Sarah Johnson",
  "payment_method": "Promo Code",
  "promo_code": "LAUNCH2026",
  "amount": "0",
  "activation_date": "2026-01-12"
}
```

**Result in Sheets**:
- ✅ Added to "Pro Users" with expiry: 2026-02-11
- ✅ Logged in "Promo Code History"
- ✅ Logged in "Payment History" (amount: 0)
- ✅ Logged in "Account Upgrades" (FREE → PRO)

---

### Scenario 2: User Pays via Razorpay

**Input**:
```json
{
  "email": "premium@example.com",
  "name": "Michael Chen",
  "payment_method": "Razorpay",
  "amount": "499",
  "transaction_id": "pay_ABC123XYZ",
  "activation_date": "2026-01-12"
}
```

**Result in Sheets**:
- ✅ Added to "Pro Users" with expiry: 2026-02-11
- ✅ NOT logged in "Promo Code History" (no promo used)
- ✅ Logged in "Payment History" with transaction ID
- ✅ Logged in "Account Upgrades" (FREE → PRO)

---

### Scenario 3: Existing User Renews

**Input** (same email as existing user):
```json
{
  "email": "existing@example.com",
  "payment_method": "Razorpay",
  "activation_date": "2026-01-15"
}
```

**Result**:
- ✅ **Updates** existing row in "Pro Users" (not duplicate)
- ✅ New expiry: 2026-02-14 (30 days from new activation)
- ✅ Days remaining reset to 30
- ✅ New entries in Payment History and Account Upgrades

---

## 📈 Analytics You Can Track

### 1. Total PRO Users
```sql
=COUNTA(Pro Users!B2:B) - 1
```

### 2. Active vs Expired
```sql
Active:  =COUNTIF(Pro Users!L:L, "ACTIVE")
Expired: =COUNTIF(Pro Users!L:L, "EXPIRED")
```

### 3. Total Revenue
```sql
=SUM(Payment History!E:E)
```

### 4. Most Popular Promo Code
```sql
=MODE(Promo Code History!D:D)
```

### 5. Conversion Rate
```sql
=(Account Upgrades Count / Total Users) * 100
```

---

## 🎨 Visual Status Indicators

### Row Color Coding

```
┌────────────────────────────────────────────────────────────┐
│ 🟢 GREEN (#e8f5e9)                                         │
│ user@example.com | PRO | 2026-02-11 | 30 days | ACTIVE    │
└────────────────────────────────────────────────────────────┘
         ↑
    Plenty of time remaining


┌────────────────────────────────────────────────────────────┐
│ 🟡 YELLOW (#fff9c4)                                        │
│ user@example.com | PRO | 2026-01-19 | 7 days | ACTIVE     │
└────────────────────────────────────────────────────────────┘
         ↑
    Expiring soon - send renewal reminder!


┌────────────────────────────────────────────────────────────┐
│ 🔴 RED (#ffebee)                                           │
│ user@example.com | PRO | 2026-01-10 | 0 days | EXPIRED    │
└────────────────────────────────────────────────────────────┘
         ↑
    Expired - downgrade to FREE
```

---

## ⏰ Daily Auto-Update Process

**Trigger**: Every day at 2:00 AM

**Actions**:
1. Loop through all users in "Pro Users" sheet
2. Recalculate "Days Remaining" based on current date
3. Update "Status" (ACTIVE → EXPIRED if needed)
4. Apply color coding based on new status
5. Log completion in Apps Script logs

**Setup**: Run `createDailyTrigger()` once

---

## 🔍 Query Examples

### Get Active Users Only
```
GET https://your-script-url/exec
```

### Get All Users
```
GET https://your-script-url/exec?action=all
```

### Get Expired Users
```
GET https://your-script-url/exec?action=expired
```

---

## 📞 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Data not saving | Check "Who has access" = "Anyone" |
| Sheets not created | Run `setupSheets()` manually |
| Wrong expiry date | Verify activation_date format (YYYY-MM-DD) |
| Duplicate entries | Script auto-detects email and updates |
| Colors not showing | Run `updateAllUserStatus()` manually |

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ 4 sheets are created with colored headers
- ✅ POST requests return success with expiry_date
- ✅ GET requests return user arrays
- ✅ Rows are color-coded automatically
- ✅ Days remaining decreases daily
- ✅ Status changes from ACTIVE to EXPIRED after 30 days

---

**🎉 Your Pro Plan tracking system is now fully automated!**

All promo codes, payments, and upgrades are tracked with 30-day validity.

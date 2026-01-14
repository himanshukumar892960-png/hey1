// ═════════════════════════════════════════════════════════════════════════════
// 🚀 GlobleXGPT Pro Plan Management System - Google Apps Script
// ═════════════════════════════════════════════════════════════════════════════
// 
// FEATURES:
// ✅ Track all promo code usage
// ✅ Record payment methods (Razorpay, Promo Code)
// ✅ Automatic 30-day validity calculation
// ✅ Account upgrade tracking
// ✅ Expiry date validation
// ✅ Comprehensive user history
// 
// DEPLOYMENT INSTRUCTIONS:
// 1. Go to https://script.google.com/home
// 2. Create a new project or open your existing Google Sheet
// 3. Go to Extensions > Apps Script
// 4. Paste this entire code into Code.gs
// 5. Save the project (Ctrl+S)
// 6. Click "Deploy" > "New deployment"
// 7. Select type: "Web app"
// 8. Set Description: "GlobleXGPT Pro Plan Manager v2.0"
// 9. Set execute as: "Me (your email)"
// 10. Set who has access: "Anyone" (CRITICAL!)
// 11. Click "Deploy" and copy the "Web app URL"
// 12. Paste URL into your .env file as GOOGLE_SHEETS_SCRIPT_URL
// 13. Run setupSheets() function once manually to create all sheets
// ═════════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// 📋 SHEET SETUP FUNCTION - Run this once manually
// ─────────────────────────────────────────────────────────────────────────────
function setupSheets() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    // Sheet 1: Pro Users (Main tracking)
    var proSheet = ss.getSheetByName("Pro Users") || ss.insertSheet("Pro Users");
    if (proSheet.getLastRow() === 0) {
        proSheet.appendRow([
            "Timestamp",
            "Email",
            "Name",
            "Phone",
            "Payment Method",
            "Amount",
            "Promo Code",
            "Plan Type",
            "Activation Date",
            "Expiry Date",
            "Days Remaining",
            "Status",
            "IP Address"
        ]);
        proSheet.getRange(1, 1, 1, 13).setFontWeight("bold").setBackground("#4285f4").setFontColor("#ffffff");
        proSheet.setFrozenRows(1);
        proSheet.setFrozenColumns(2);
    }

    // Sheet 2: Promo Code Usage History
    var promoSheet = ss.getSheetByName("Promo Code History") || ss.insertSheet("Promo Code History");
    if (promoSheet.getLastRow() === 0) {
        promoSheet.appendRow([
            "Timestamp",
            "Email",
            "Name",
            "Promo Code Used",
            "Activation Date",
            "Expiry Date",
            "Status"
        ]);
        promoSheet.getRange(1, 1, 1, 7).setFontWeight("bold").setBackground("#34a853").setFontColor("#ffffff");
        promoSheet.setFrozenRows(1);
    }

    // Sheet 3: Payment History
    var paymentSheet = ss.getSheetByName("Payment History") || ss.insertSheet("Payment History");
    if (paymentSheet.getLastRow() === 0) {
        paymentSheet.appendRow([
            "Timestamp",
            "Email",
            "Name",
            "Payment Method",
            "Amount",
            "Transaction ID",
            "Status",
            "IP Address"
        ]);
        paymentSheet.getRange(1, 1, 1, 8).setFontWeight("bold").setBackground("#fbbc04").setFontColor("#ffffff");
        paymentSheet.setFrozenRows(1);
    }

    // Sheet 4: Account Upgrades
    var upgradeSheet = ss.getSheetByName("Account Upgrades") || ss.insertSheet("Account Upgrades");
    if (upgradeSheet.getLastRow() === 0) {
        upgradeSheet.appendRow([
            "Timestamp",
            "Email",
            "Name",
            "Previous Plan",
            "New Plan",
            "Upgrade Method",
            "Validity Period"
        ]);
        upgradeSheet.getRange(1, 1, 1, 7).setFontWeight("bold").setBackground("#ea4335").setFontColor("#ffffff");
        upgradeSheet.setFrozenRows(1);
    }

    Logger.log("✅ All sheets created successfully!");
}

// ─────────────────────────────────────────────────────────────────────────────
// 🔧 HELPER FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────

// Calculate expiry date (30 days from activation)
function calculateExpiryDate(activationDate) {
    var date = new Date(activationDate);
    date.setDate(date.getDate() + 30);
    return date.toISOString().split('T')[0];
}

// Calculate days remaining
function calculateDaysRemaining(expiryDate) {
    var today = new Date();
    var expiry = new Date(expiryDate);
    var diffTime = expiry - today;
    var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
}

// Check if plan is active
function isPlanActive(expiryDate) {
    var today = new Date();
    var expiry = new Date(expiryDate);
    return expiry > today ? "ACTIVE" : "EXPIRED";
}

// Format timestamp
function getTimestamp() {
    return new Date().toISOString();
}

// ─────────────────────────────────────────────────────────────────────────────
// 📨 POST REQUEST HANDLER - Receive data from Python backend
// ─────────────────────────────────────────────────────────────────────────────
function doPost(e) {
    var lock = LockService.getScriptLock();
    lock.tryLock(10000);

    try {
        var data = JSON.parse(e.postData.contents);
        var ss = SpreadsheetApp.getActiveSpreadsheet();

        // Extract data
        var timestamp = data.timestamp || getTimestamp();
        var email = data.email || "";
        var name = data.name || "";
        var phone = data.phone || "";
        var paymentMethod = data.payment_method || "Unknown";
        var amount = data.amount || "0";
        var promoCode = data.promo_code || "N/A";
        var planType = data.plan_type || "PRO";
        var activationDate = data.activation_date || new Date().toISOString().split('T')[0];
        var expiryDate = data.expiry_date || calculateExpiryDate(activationDate);
        var ipAddress = data.ip_address || "";
        var transactionId = data.transaction_id || "";

        // Calculate dynamic fields
        var daysRemaining = calculateDaysRemaining(expiryDate);
        var status = isPlanActive(expiryDate);

        // ═══════════════════════════════════════════════════════════════════════
        // 1️⃣ UPDATE PRO USERS SHEET
        // ═══════════════════════════════════════════════════════════════════════
        var proSheet = ss.getSheetByName("Pro Users");
        if (!proSheet) {
            setupSheets();
            proSheet = ss.getSheetByName("Pro Users");
        }

        // Check if user already exists
        var proData = proSheet.getDataRange().getValues();
        var userExists = false;
        var userRow = -1;

        for (var i = 1; i < proData.length; i++) {
            if (proData[i][1] === email) { // Column B (Email)
                userExists = true;
                userRow = i + 1;
                break;
            }
        }

        if (userExists) {
            // Update existing user
            proSheet.getRange(userRow, 1, 1, 13).setValues([[
                timestamp, email, name, phone, paymentMethod, amount, promoCode,
                planType, activationDate, expiryDate, daysRemaining, status, ipAddress
            ]]);
        } else {
            // Add new user
            proSheet.appendRow([
                timestamp, email, name, phone, paymentMethod, amount, promoCode,
                planType, activationDate, expiryDate, daysRemaining, status, ipAddress
            ]);
        }

        // ═══════════════════════════════════════════════════════════════════════
        // 2️⃣ LOG PROMO CODE USAGE (if applicable)
        // ═══════════════════════════════════════════════════════════════════════
        if (promoCode !== "N/A" && paymentMethod.toLowerCase().includes("promo")) {
            var promoSheet = ss.getSheetByName("Promo Code History");
            promoSheet.appendRow([
                timestamp, email, name, promoCode, activationDate, expiryDate, status
            ]);
        }

        // ═══════════════════════════════════════════════════════════════════════
        // 3️⃣ LOG PAYMENT HISTORY
        // ═══════════════════════════════════════════════════════════════════════
        var paymentSheet = ss.getSheetByName("Payment History");
        paymentSheet.appendRow([
            timestamp, email, name, paymentMethod, amount, transactionId, "SUCCESS", ipAddress
        ]);

        // ═══════════════════════════════════════════════════════════════════════
        // 4️⃣ LOG ACCOUNT UPGRADE
        // ═══════════════════════════════════════════════════════════════════════
        var upgradeSheet = ss.getSheetByName("Account Upgrades");
        upgradeSheet.appendRow([
            timestamp, email, name, "FREE", planType, paymentMethod, "30 Days"
        ]);

        return ContentService
            .createTextOutput(JSON.stringify({
                'result': 'success',
                'message': 'Pro plan activated successfully',
                'expiry_date': expiryDate,
                'days_remaining': daysRemaining,
                'status': status
            }))
            .setMimeType(ContentService.MimeType.JSON);

    } catch (error) {
        return ContentService
            .createTextOutput(JSON.stringify({
                'result': 'error',
                'error': error.toString()
            }))
            .setMimeType(ContentService.MimeType.JSON);
    } finally {
        lock.releaseLock();
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// 📥 GET REQUEST HANDLER - Return active PRO users
// ─────────────────────────────────────────────────────────────────────────────
function doGet(e) {
    try {
        var ss = SpreadsheetApp.getActiveSpreadsheet();
        var proSheet = ss.getSheetByName("Pro Users");

        if (!proSheet) {
            return ContentService
                .createTextOutput(JSON.stringify({ 'result': 'error', 'message': 'Sheet not found. Run setupSheets() first.' }))
                .setMimeType(ContentService.MimeType.JSON);
        }

        var rows = proSheet.getDataRange().getValues();
        var activeUsers = [];
        var expiredUsers = [];
        var allUsers = [];

        // Skip header row
        for (var i = 1; i < rows.length; i++) {
            var row = rows[i];
            var email = row[1];
            var name = row[2];
            var planType = row[7];
            var expiryDate = row[9];
            var daysRemaining = calculateDaysRemaining(expiryDate);
            var status = isPlanActive(expiryDate);

            var userObj = {
                email: email,
                name: name,
                plan_type: planType,
                expiry_date: expiryDate,
                days_remaining: daysRemaining,
                status: status
            };

            allUsers.push(userObj);

            if (status === "ACTIVE") {
                activeUsers.push(userObj);
            } else {
                expiredUsers.push(userObj);
            }
        }

        // Check if specific action requested
        var action = e.parameter.action || "active";

        if (action === "all") {
            return ContentService
                .createTextOutput(JSON.stringify(allUsers))
                .setMimeType(ContentService.MimeType.JSON);
        } else if (action === "expired") {
            return ContentService
                .createTextOutput(JSON.stringify(expiredUsers))
                .setMimeType(ContentService.MimeType.JSON);
        } else {
            // Default: return only active users
            return ContentService
                .createTextOutput(JSON.stringify(activeUsers))
                .setMimeType(ContentService.MimeType.JSON);
        }

    } catch (error) {
        return ContentService
            .createTextOutput(JSON.stringify({ 'result': 'error', 'error': error.toString() }))
            .setMimeType(ContentService.MimeType.JSON);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// 🔄 AUTO-UPDATE FUNCTION - Run daily to update status
// ─────────────────────────────────────────────────────────────────────────────
function updateAllUserStatus() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var proSheet = ss.getSheetByName("Pro Users");

    if (!proSheet) return;

    var rows = proSheet.getDataRange().getValues();

    for (var i = 1; i < rows.length; i++) {
        var expiryDate = rows[i][9]; // Column J
        var daysRemaining = calculateDaysRemaining(expiryDate);
        var status = isPlanActive(expiryDate);

        // Update columns K and L
        proSheet.getRange(i + 1, 11).setValue(daysRemaining);
        proSheet.getRange(i + 1, 12).setValue(status);

        // Color code based on status
        if (status === "EXPIRED") {
            proSheet.getRange(i + 1, 1, 1, 13).setBackground("#ffebee"); // Light red
        } else if (daysRemaining <= 7) {
            proSheet.getRange(i + 1, 1, 1, 13).setBackground("#fff9c4"); // Light yellow
        } else {
            proSheet.getRange(i + 1, 1, 1, 13).setBackground("#e8f5e9"); // Light green
        }
    }

    Logger.log("✅ User status updated successfully!");
}

// ─────────────────────────────────────────────────────────────────────────────
// ⏰ CREATE DAILY TRIGGER - Run this once to auto-update daily
// ─────────────────────────────────────────────────────────────────────────────
function createDailyTrigger() {
    // Delete existing triggers
    var triggers = ScriptApp.getProjectTriggers();
    for (var i = 0; i < triggers.length; i++) {
        ScriptApp.deleteTrigger(triggers[i]);
    }

    // Create new daily trigger at 2 AM
    ScriptApp.newTrigger('updateAllUserStatus')
        .timeBased()
        .atHour(2)
        .everyDays(1)
        .create();

    Logger.log("✅ Daily trigger created successfully!");
}

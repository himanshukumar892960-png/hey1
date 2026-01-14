# FIXED: "Error 400: origin_mismatch"

This error happens because your Google Cloud settings strictly strictly block any URL that is not explicitly whitelisted. 

### **Step 1: Open Google Cloud Console**
1. Go to this link: [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Make sure the project selected at the top-left is the one with Client ID: `307616482502-...`
3. Under **"OAuth 2.0 Client IDs"**, find your client (Web client 1) and click the **Pencil Icon** (Edit).

### **Step 2: Add 'Authorized JavaScript origins' (CRITICAL)**
You must add **BOTH** of these exactly as written. **Do not add a trailing slash `/`**.

1. Click **ADD URI** under "Authorized JavaScript origins".
2. Paste: 
   ```
   http://localhost:5000
   ```
3. Click **ADD URI** again.
4. Paste:
   ```
   http://127.0.0.1:5000
   ```

### **Step 3: Save and Wait (CRITICAL)**
1. Click the blue **SAVE** button at the bottom.
2. **WAIT 5 MINUTES.** Google takes time to update this setting worldwide.
3. Restart your Python app (`Ctrl+C` in terminal, then run it again).
4. **Hard Refresh** your browser (`Ctrl+F5`) or open an **Incognito Window** to test.

### **Common Mistakes to Avoid**
*   **Do NOT** add `http://localhost:5000/` (No slash at the end!)
*   **Do NOT** use `https` if you are running on `http`.
*   **Do NOT** add `google.com` or other random URLs. Just your local server.

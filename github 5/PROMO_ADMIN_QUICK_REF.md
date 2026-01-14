# 🔐 Quick Reference - Promo Code Admin

## Secret Code
```
Abinav_9009
```

## How to Change Promo Code

1. **Open**: Click "Upgrade to Pro" button
2. **Scroll**: Go to bottom of modal
3. **Expand**: Click "🔐 Admin: Change Promo Code"
4. **Enter**:
   - Secret Code: `Abinav_9009`
   - New Promo Code: (your new code)
5. **Update**: Click "Update Promo Code"

## Current Active Code

Check in browser console:
```javascript
localStorage.getItem('active_promo_code')
```

Default: `HimanshuFree`

## Reset to Default

```javascript
localStorage.setItem('active_promo_code', 'HimanshuFree')
```

## Files Modified
- `templates/index.html` - Admin UI
- `static/js/main.js` - Admin logic

---

**⚠️ Keep Secret Code Confidential**

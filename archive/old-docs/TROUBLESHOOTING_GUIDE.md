# Troubleshooting Guide - Fixing All Errors

## Current Errors You're Experiencing

1. ❌ **Upload failed: new row violates row-level security policy**
2. ❌ **Forecast request failed: Failed to send a request to the Edge Function**
3. ❌ **Application Failed: Failed to submit application**
4. ❌ **Profile update error persists**
5. ❌ **Report still saving as JSON instead of Excel**

---

## 🔧 SOLUTION: Apply Database Fixes

### Step 1: Apply SQL Fixes in Supabase Dashboard

1. **Go to your Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project**
3. **Click on "SQL Editor" in the left sidebar**
4. **Click "New Query"**
5. **Copy the ENTIRE contents** of `APPLY_FIXES_MANUALLY.sql` file
6. **Paste into the SQL Editor**
7. **Click "Run"** (or press Ctrl+Enter)

This will:
- ✅ Create the `vat_applications` table with proper RLS policies
- ✅ Fix the `profiles` table RLS policies
- ✅ Fix storage policies for document and avatar uploads
- ✅ Show verification results at the end

### Step 2: Verify the Fixes

After running the SQL script, you should see output like:

```
vat_applications table exists
profiles table exists
VAT Applications policies: 3
Profiles policies: 3
Storage policies: 4
```

If you see these messages, the database is fixed! ✅

---

## 🚀 SOLUTION: Deploy Edge Function

The forecast error happens because the Edge Function isn't deployed yet.

### Option A: Using Supabase CLI (Recommended)

```powershell
# Navigate to web directory
cd c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web

# Deploy the Edge Function
npx supabase functions deploy user-vat-forecast
```

### Option B: Manual Deployment via Dashboard

1. Go to **Supabase Dashboard** → **Edge Functions**
2. Click **"Create a new function"**
3. Name it: `user-vat-forecast`
4. Copy the entire contents of `web/supabase/functions/user-vat-forecast/index.ts`
5. Paste into the function editor
6. Click **"Deploy"**

---

## 📊 SOLUTION: Excel Export Issue

If reports are still saving as JSON, it means the browser is caching the old code.

### Fix:

1. **Hard refresh the browser**:
   - Windows: `Ctrl + Shift + R` or `Ctrl + F5`
   - Mac: `Cmd + Shift + R`

2. **Clear browser cache**:
   - Chrome: Settings → Privacy → Clear browsing data → Cached images and files
   - Firefox: Settings → Privacy → Clear Data → Cached Web Content

3. **Restart the dev server**:
   ```powershell
   # Stop the server (Ctrl+C)
   # Then restart
   npm run dev
   ```

4. **Verify XLSX is installed**:
   ```powershell
   npm list xlsx
   ```
   Should show: `xlsx@0.18.5`

---

## 🧪 Testing After Fixes

### Test 1: Profile Photo Upload
1. Go to Profile page
2. Click "Edit Profile"
3. Click on the avatar to upload a photo
4. Select an image (under 5MB)
5. ✅ Should show "Photo Updated" toast
6. ❌ If error: Check SQL script was run correctly

### Test 2: Profile Update
1. Edit your name, department, or position
2. Click "Save Changes"
3. ✅ Should show "Profile updated successfully"
4. ❌ If error: Check SQL script was run correctly

### Test 3: VAT Application Submission
1. Fill out the VAT Refund Predictor form
2. Click "Calculate Refund"
3. Click "Start Application"
4. ✅ Should show "Application Submitted Successfully"
5. ❌ If error: Check SQL script was run correctly

### Test 4: Excel Report Export
1. After calculating a refund prediction
2. Click "Save Report"
3. ✅ Should download a `.xlsx` file (not `.json`)
4. ✅ Open the file in Excel - should have formatted data
5. ❌ If still JSON: Hard refresh browser (Ctrl+Shift+R)

### Test 5: VAT Forecast
1. Go to Dashboard
2. Look at the "VAT Collection Forecast" chart
3. ✅ Should load without errors
4. ✅ Should show message about uploading documents
5. ❌ If error: Check Edge Function is deployed

---

## 🔍 Detailed Error Diagnosis

### Error: "new row violates row-level security policy"

**Cause**: RLS policies are missing or incorrect

**Solution**: 
1. Run the `APPLY_FIXES_MANUALLY.sql` script
2. Verify policies exist:
   ```sql
   SELECT tablename, policyname 
   FROM pg_policies 
   WHERE schemaname = 'public' 
   AND tablename IN ('vat_applications', 'profiles');
   ```

### Error: "Failed to send a request to the Edge Function"

**Cause**: Edge Function not deployed

**Solution**:
1. Deploy using: `npx supabase functions deploy user-vat-forecast`
2. Or deploy manually via dashboard
3. Verify in Dashboard → Edge Functions → Should see `user-vat-forecast`

### Error: Report saves as JSON instead of Excel

**Cause**: Browser cache or XLSX not imported

**Solution**:
1. Hard refresh: `Ctrl + Shift + R`
2. Check import in `VATRefundPredictor.tsx`:
   ```typescript
   import * as XLSX from 'xlsx';
   ```
3. Verify XLSX is installed: `npm list xlsx`

---

## 📋 Verification Checklist

After applying all fixes, verify:

- [ ] SQL script ran successfully in Supabase Dashboard
- [ ] `vat_applications` table exists
- [ ] `profiles` table has RLS policies
- [ ] Storage policies allow avatar uploads
- [ ] Edge Function `user-vat-forecast` is deployed
- [ ] Browser cache cleared (hard refresh)
- [ ] Dev server restarted
- [ ] Profile photo upload works
- [ ] Profile update works
- [ ] Application submission works
- [ ] Excel export works (downloads .xlsx file)
- [ ] Forecast chart loads without errors

---

## 🆘 Still Having Issues?

### Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for error messages
4. Common errors and fixes:

**"Failed to fetch"**
- Check if dev server is running
- Check if Supabase URL is correct in `.env`

**"Invalid API key"**
- Check Supabase anon key in `.env`
- Verify project URL matches

**"Not authenticated"**
- Log out and log back in
- Check if session is valid

### Check Network Tab

1. Open DevTools → Network tab
2. Try the failing action
3. Look for failed requests (red)
4. Click on failed request → Preview tab
5. Check error message

### Check Supabase Logs

1. Go to Supabase Dashboard
2. Click "Logs" in sidebar
3. Select "Edge Functions" or "Database"
4. Look for error messages

---

## 📞 Quick Reference

### File Locations
- SQL Fix Script: `APPLY_FIXES_MANUALLY.sql`
- Edge Function: `web/supabase/functions/user-vat-forecast/index.ts`
- VAT Predictor: `web/src/components/VATRefundPredictor.tsx`
- Profile Page: `web/src/pages/Profile.tsx`
- Forecast Chart: `web/src/components/PredictiveChart.tsx`

### Commands
```powershell
# Install dependencies
npm install

# Run dev server
npm run dev

# Deploy Edge Function
npx supabase functions deploy user-vat-forecast

# Check XLSX installation
npm list xlsx
```

### Supabase Dashboard URLs
- SQL Editor: https://supabase.com/dashboard/project/YOUR_PROJECT/sql
- Edge Functions: https://supabase.com/dashboard/project/YOUR_PROJECT/functions
- Storage: https://supabase.com/dashboard/project/YOUR_PROJECT/storage
- Logs: https://supabase.com/dashboard/project/YOUR_PROJECT/logs

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ Profile photo uploads without errors
2. ✅ Profile updates save successfully
3. ✅ "Start Application" saves to database
4. ✅ "Save Report" downloads Excel file (`.xlsx`)
5. ✅ Forecast chart loads without errors
6. ✅ No RLS policy errors in console
7. ✅ No Edge Function errors in console

---

## 🎯 Priority Order

If you're short on time, fix in this order:

1. **CRITICAL**: Run `APPLY_FIXES_MANUALLY.sql` (fixes 4 out of 5 errors)
2. **HIGH**: Deploy Edge Function (fixes forecast error)
3. **MEDIUM**: Hard refresh browser (fixes Excel export)

This should resolve all your issues! 🎉
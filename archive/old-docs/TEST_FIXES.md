# Test Plan - Verify All Fixes Work

## Before Testing

1. ✅ Run `APPLY_FIXES_MANUALLY.sql` in Supabase Dashboard
2. ✅ Deploy Edge Function (if possible)
3. ✅ Hard refresh browser (Ctrl+Shift+R)
4. ✅ Make sure dev server is running

---

## Test 1: Profile Photo Upload ✅

**Steps:**
1. Navigate to Profile page
2. Click "Edit Profile" button
3. Click on the avatar/profile picture area
4. Select an image file (JPG, PNG, under 5MB)
5. Wait for upload

**Expected Result:**
- ✅ Toast notification: "Uploading..."
- ✅ Toast notification: "Photo Updated"
- ✅ Profile picture changes to uploaded image
- ✅ No errors in console

**If it fails:**
- Check browser console for error message
- Verify SQL script was run
- Check storage policies in Supabase Dashboard

---

## Test 2: Profile Information Update ✅

**Steps:**
1. On Profile page, click "Edit Profile"
2. Change your name to something different
3. Change department (e.g., "Engineering")
4. Change position (e.g., "Senior Developer")
5. Click "Save Changes"

**Expected Result:**
- ✅ Toast notification: "Profile updated successfully"
- ✅ Changes are visible immediately
- ✅ Refresh page - changes persist
- ✅ No errors in console

**If it fails:**
- Check browser console for "RLS policy" error
- Verify SQL script was run
- Check profiles table policies in Supabase

---

## Test 3: VAT Application Submission ✅

**Steps:**
1. Navigate to VAT Refund Predictor
2. Fill in the form:
   - Business Type: "Retail"
   - Annual Turnover: "5000000"
   - VAT Paid: "500000"
   - Input VAT: "400000"
   - Category: "Electronics"
   - Region: "Maharashtra"
   - Filing Status: "Filed"
3. Click "Calculate Refund"
4. Wait for prediction results
5. Click "Start Application" button

**Expected Result:**
- ✅ Button shows "Submitting..."
- ✅ Toast notification: "Application Submitted Successfully"
- ✅ Message mentions tracking in dashboard
- ✅ No errors in console

**If it fails:**
- Check browser console for "RLS policy" error
- Verify SQL script was run
- Check vat_applications table exists in Supabase

---

## Test 4: Excel Report Export ✅

**Steps:**
1. After calculating a VAT refund (from Test 3)
2. Click "Save Report" button
3. Check your Downloads folder

**Expected Result:**
- ✅ File downloads immediately
- ✅ Filename: `vat-refund-report-2025-01-XX.xlsx` (NOT .json)
- ✅ Toast notification: "Report Saved"
- ✅ Open file in Excel/LibreOffice:
  - Should have formatted data
  - Should have sections: Prediction Details, Input Details, Model Information, Risk Factors
  - Should have proper column widths
- ✅ No errors in console

**If it fails (still downloads JSON):**
- Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear browser cache completely
- Restart dev server
- Check if XLSX is imported in VATRefundPredictor.tsx

---

## Test 5: VAT Collection Forecast ✅

**Steps:**
1. Navigate to Dashboard
2. Scroll to "VAT Collection Forecast" chart
3. Observe the chart and any messages

**Expected Result:**
- ✅ Chart loads without errors
- ✅ Shows forecast data (bars/lines)
- ✅ Shows message: "No VAT documents uploaded yet" (if you haven't uploaded any)
- ✅ OR shows: "Personalized predictions based on X documents" (if you have uploaded VAT docs)
- ✅ No errors in console

**If it fails:**
- Check browser console for "Edge Function" error
- Verify Edge Function is deployed
- Check Supabase Dashboard → Edge Functions → user-vat-forecast should exist
- Check Supabase logs for function errors

---

## Test 6: Document Upload (Bonus) ✅

**Steps:**
1. Navigate to Document Upload page
2. Click "Upload Document"
3. Select a PDF file
4. Choose document type: "VAT Return"
5. Click "Upload"

**Expected Result:**
- ✅ File uploads successfully
- ✅ Shows in document list
- ✅ Can view/download the document
- ✅ No errors in console

**If it fails:**
- Check storage policies in Supabase
- Verify SQL script was run
- Check browser console for errors

---

## Verification Checklist

After running all tests, check:

### Database Tables
```sql
-- Run in Supabase SQL Editor
SELECT COUNT(*) as vat_applications_count FROM vat_applications;
SELECT COUNT(*) as profiles_count FROM profiles;
```

### Storage
- Go to Supabase Dashboard → Storage → documents bucket
- Should see folders: `avatars/`, `[your-user-id]/`
- Avatars folder should have your uploaded profile picture

### Edge Functions
- Go to Supabase Dashboard → Edge Functions
- Should see: `user-vat-forecast` (deployed)
- Click on it → Check logs for any errors

---

## Common Issues and Quick Fixes

### Issue: "RLS policy violation"
**Fix:** Run `APPLY_FIXES_MANUALLY.sql` in Supabase SQL Editor

### Issue: "Edge Function failed"
**Fix:** Deploy function: `npx supabase functions deploy user-vat-forecast`

### Issue: "Still downloads JSON"
**Fix:** Hard refresh browser (Ctrl+Shift+R) and clear cache

### Issue: "Not authenticated"
**Fix:** Log out and log back in

### Issue: "File too large"
**Fix:** Use image under 5MB for profile photo

---

## Success Criteria

✅ **All tests pass** = Everything is working correctly!

If any test fails:
1. Check the specific "If it fails" section for that test
2. Review browser console for error messages
3. Check Supabase logs
4. Refer to `TROUBLESHOOTING_GUIDE.md`

---

## Test Results Template

Copy this and fill in your results:

```
Test 1 - Profile Photo Upload: [ ] PASS [ ] FAIL
Test 2 - Profile Update: [ ] PASS [ ] FAIL
Test 3 - Application Submission: [ ] PASS [ ] FAIL
Test 4 - Excel Export: [ ] PASS [ ] FAIL
Test 5 - Forecast Chart: [ ] PASS [ ] FAIL
Test 6 - Document Upload: [ ] PASS [ ] FAIL

Notes:
- 
- 
- 
```

---

## Next Steps After All Tests Pass

1. ✅ Commit your changes to git
2. ✅ Deploy to production (if ready)
3. ✅ Test in production environment
4. ✅ Monitor Supabase logs for any issues
5. ✅ Celebrate! 🎉

---

## Need Help?

If tests are failing:
1. Check `TROUBLESHOOTING_GUIDE.md`
2. Review browser console errors
3. Check Supabase Dashboard logs
4. Verify all SQL scripts ran successfully
5. Ensure Edge Function is deployed
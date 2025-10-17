# Deployment Guide for Critical Fixes

## Prerequisites

Before deploying, ensure you have:
1. Supabase CLI installed
2. Supabase project initialized
3. Database connection configured

## Step 1: Install Supabase CLI (if not already installed)

### Windows (PowerShell)
```powershell
# Using Scoop
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase

# OR using npm
npm install -g supabase
```

### Verify Installation
```powershell
supabase --version
```

## Step 2: Link to Your Supabase Project

```powershell
# Navigate to web directory
Set-Location "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web"

# Link to your project (you'll need your project ref)
supabase link --project-ref YOUR_PROJECT_REF

# OR login and select project interactively
supabase login
supabase link
```

## Step 3: Deploy Database Migration

```powershell
# Push the migration to add profile columns
supabase db push

# OR apply specific migration
supabase migration up
```

**What this does:**
- Adds 5 new columns to the `profiles` table: phone, department, position, location, join_date
- Migration is idempotent (safe to run multiple times)

## Step 4: Deploy Edge Function

```powershell
# Deploy the user-vat-forecast function
supabase functions deploy user-vat-forecast

# Verify deployment
supabase functions list
```

**What this does:**
- Deploys the `user-vat-forecast` Edge Function to Supabase
- This function analyzes user's VAT documents and generates personalized forecasts

## Step 5: Set Environment Variables (if needed)

The Edge Function uses these environment variables (automatically available in Supabase):
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Your Supabase anonymous key

These are automatically set by Supabase, but you can verify:

```powershell
supabase functions env list
```

## Step 6: Test the Deployment

### Test Database Migration
```powershell
# Check if columns were added
supabase db diff
```

### Test Edge Function
```powershell
# Test the function locally first
supabase functions serve user-vat-forecast

# In another terminal, test with curl
curl -i --location --request POST 'http://localhost:54321/functions/v1/user-vat-forecast' `
  --header 'Authorization: Bearer YOUR_ANON_KEY' `
  --header 'Content-Type: application/json' `
  --data '{"start_month":"2025-01","num_months":8}'
```

## Step 7: Restart Your Development Server

```powershell
# Navigate to web directory
Set-Location "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\web"

# Install dependencies if needed
npm install

# Start development server
npm run dev
```

## Verification Checklist

After deployment, verify each fix:

### ✅ Profile Saving
1. Open the application and navigate to Profile page
2. Edit any field (name, email, phone, etc.)
3. Click "Save" button
4. Refresh the page
5. **Expected:** All changes should persist

### ✅ VAT Forecast with User Data
1. Navigate to Dashboard
2. Look at the "VAT Collection Forecast" chart
3. **If you have uploaded VAT documents:**
   - Should show "Personalized predictions based on X documents"
4. **If you have NO documents:**
   - Should show alert "Upload VAT refund documents to get personalized forecasts"

### ✅ Anomaly Detection Details
1. Navigate to Dashboard
2. Find the "Anomaly Detection" metric card
3. Click on it (if it shows alerts)
4. **Expected:** Dialog opens showing list of problematic documents with details

### ✅ VAT Refund Predictor Buttons
1. Navigate to VAT Refund Predictor page
2. Click "Start Application" button
3. **Expected:** Toast notification appears
4. Click "Save Report" button
5. **Expected:** JSON file downloads with prediction data

## Troubleshooting

### Issue: Migration fails with "column already exists"
**Solution:** This is normal if migration was already applied. The migration uses `IF NOT EXISTS` so it's safe.

### Issue: Edge Function returns 404
**Solution:** 
1. Verify function was deployed: `supabase functions list`
2. Check function logs: `supabase functions logs user-vat-forecast`
3. Redeploy: `supabase functions deploy user-vat-forecast`

### Issue: Profile still doesn't save
**Solution:**
1. Check browser console for errors
2. Verify user is authenticated
3. Check Supabase dashboard for database errors
4. Verify migration ran: `supabase db diff`

### Issue: Forecast still shows generic data
**Solution:**
1. Verify Edge Function is deployed
2. Check that you have VAT documents uploaded
3. Check browser console for errors
4. Verify documents have `type` containing "VAT"

### Issue: "Not authenticated" error
**Solution:**
1. Ensure user is logged in
2. Check Supabase auth configuration
3. Verify JWT token is being sent in requests

## Alternative: Manual Deployment

If Supabase CLI doesn't work, you can deploy manually:

### Manual Database Migration
1. Go to Supabase Dashboard → SQL Editor
2. Copy contents of `web/supabase/migrations/20250103000000_extend_profiles_table.sql`
3. Paste and run in SQL Editor

### Manual Edge Function Deployment
1. Go to Supabase Dashboard → Edge Functions
2. Create new function named `user-vat-forecast`
3. Copy contents of `web/supabase/functions/user-vat-forecast/index.ts`
4. Paste and deploy

## Rollback (if needed)

### Rollback Database Migration
```powershell
# Create rollback migration
supabase migration new rollback_profile_columns

# Edit the new migration file and add:
# ALTER TABLE profiles DROP COLUMN IF EXISTS phone;
# ALTER TABLE profiles DROP COLUMN IF EXISTS department;
# ALTER TABLE profiles DROP COLUMN IF EXISTS position;
# ALTER TABLE profiles DROP COLUMN IF EXISTS location;
# ALTER TABLE profiles DROP COLUMN IF EXISTS join_date;

# Apply rollback
supabase db push
```

### Remove Edge Function
```powershell
supabase functions delete user-vat-forecast
```

## Production Deployment

For production deployment:

1. **Test thoroughly in development first**
2. **Backup your database** before running migrations
3. **Deploy during low-traffic period**
4. **Monitor logs** after deployment:
   ```powershell
   supabase functions logs user-vat-forecast --follow
   ```
5. **Have rollback plan ready**

## Support

If you encounter issues:
1. Check Supabase Dashboard logs
2. Check browser console for frontend errors
3. Review `FIXES_COMPLETED.md` for implementation details
4. Check Supabase documentation: https://supabase.com/docs

---

**Once deployed, all 5 critical UX issues will be resolved!**
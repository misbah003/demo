# Error Diagnosis & Root Causes

## 🔍 Understanding Your Errors

### Error 1: "new row violates row-level security policy"

```
❌ ERROR: Upload failed: new row violates row-level security policy

WHERE IT HAPPENS:
- Profile photo upload
- Profile information update  
- VAT application submission

ROOT CAUSE:
The database tables have Row Level Security (RLS) enabled, but the 
policies that allow users to insert/update their own data are either:
1. Missing completely
2. Incomplete (missing WITH CHECK clause)
3. Not applied yet (migrations not run)

TECHNICAL EXPLANATION:
When you try to insert a row into a table with RLS enabled, Postgres
checks two things:
1. USING clause - Can you see this row?
2. WITH CHECK clause - Can you create/modify this row?

Your current policies only have USING clause, missing WITH CHECK.

SOLUTION:
Run APPLY_FIXES_MANUALLY.sql which adds proper policies with both
USING and WITH CHECK clauses.
```

---

### Error 2: "Failed to send a request to the Edge Function"

```
❌ ERROR: Forecast request failed: Failed to send a request to the Edge Function

WHERE IT HAPPENS:
- Dashboard → VAT Collection Forecast chart
- When chart tries to load forecast data

ROOT CAUSE:
The Edge Function 'user-vat-forecast' exists in your code but is not
deployed to Supabase servers.

FLOW:
1. Frontend calls: supabase.functions.invoke('user-vat-forecast')
2. Supabase looks for deployed function named 'user-vat-forecast'
3. Function not found → Error

TECHNICAL EXPLANATION:
Edge Functions must be explicitly deployed to Supabase. Having the
code in your local project is not enough - it needs to be uploaded
to Supabase's Deno runtime environment.

SOLUTION:
Deploy the function using:
npx supabase functions deploy user-vat-forecast
```

---

### Error 3: "Failed to submit application"

```
❌ ERROR: Application Failed - Failed to submit application. Please try again.

WHERE IT HAPPENS:
- VAT Refund Predictor → After calculating → Click "Start Application"

ROOT CAUSE:
Same as Error 1 - RLS policy violation when trying to insert into
vat_applications table.

FLOW:
1. User clicks "Start Application"
2. Code tries: INSERT INTO vat_applications (user_id, ...)
3. RLS checks: Does policy allow this insert?
4. Policy missing or incomplete → Error

TECHNICAL EXPLANATION:
The vat_applications table was created with RLS enabled, but the
INSERT policy either:
- Doesn't exist
- Exists but missing WITH CHECK clause
- Wasn't applied (migration not run)

SOLUTION:
Run APPLY_FIXES_MANUALLY.sql which creates the table and policies.
```

---

### Error 4: "Profile update error persists"

```
❌ ERROR: Profile update fails with RLS policy violation

WHERE IT HAPPENS:
- Profile page → Edit Profile → Save Changes

ROOT CAUSE:
Same as Error 1 - profiles table has RLS but incomplete policies.

FLOW:
1. User edits profile information
2. Code tries: UPDATE profiles SET ... WHERE user_id = ?
3. RLS checks UPDATE policy
4. Policy missing WITH CHECK clause → Error

TECHNICAL EXPLANATION:
UPDATE policies need both:
- USING: Can you access this row?
- WITH CHECK: Can you modify it to these new values?

Your current policy only has USING clause.

SOLUTION:
Run APPLY_FIXES_MANUALLY.sql which fixes the profiles policies.
```

---

### Error 5: "Report still saving as JSON"

```
❌ ERROR: Report downloads as .json file instead of .xlsx

WHERE IT HAPPENS:
- VAT Refund Predictor → After calculating → Click "Save Report"

ROOT CAUSE:
Browser is serving cached JavaScript code that has the old JSON
export logic instead of the new Excel export logic.

FLOW:
1. User clicks "Save Report"
2. Browser executes cached JavaScript
3. Cached code has old logic: downloadAsJSON()
4. New code has: XLSX.writeFile()
5. Browser doesn't know about new code → Uses old cached version

TECHNICAL EXPLANATION:
Modern browsers aggressively cache JavaScript files for performance.
When you update code, the browser may continue serving the old
cached version until you force a refresh.

SOLUTION:
Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
This forces browser to fetch fresh JavaScript files.
```

---

## 🔗 Error Relationships

```
RLS Policy Issues (Root Cause)
    ├── Error 1: Profile photo upload fails
    ├── Error 3: Application submission fails
    └── Error 4: Profile update fails

Edge Function Not Deployed (Root Cause)
    └── Error 2: Forecast request fails

Browser Cache (Root Cause)
    └── Error 5: Report saves as JSON
```

---

## 🛠️ Fix Priority & Impact

### Priority 1: Fix RLS Policies (Fixes 3 errors)
**Impact:** HIGH - Blocks core functionality
**Time:** 2 minutes
**Action:** Run APPLY_FIXES_MANUALLY.sql

### Priority 2: Deploy Edge Function (Fixes 1 error)
**Impact:** MEDIUM - Forecast feature broken
**Time:** 2 minutes
**Action:** Deploy user-vat-forecast function

### Priority 3: Clear Cache (Fixes 1 error)
**Impact:** LOW - Workaround exists (still downloads data)
**Time:** 1 minute
**Action:** Hard refresh browser

---

## 📊 Technical Deep Dive

### RLS Policy Structure

**Incorrect (Current):**
```sql
CREATE POLICY "Users can update their own profile" 
  ON public.profiles 
  FOR UPDATE 
  USING (auth.uid() = user_id);
  -- ❌ Missing WITH CHECK clause
```

**Correct (Fixed):**
```sql
CREATE POLICY "Users can update their own profile" 
  ON public.profiles 
  FOR UPDATE 
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
  -- ✅ Has both USING and WITH CHECK
```

### Why Both Clauses Matter

- **USING**: "Can you see/access this row?"
  - Checked when reading (SELECT)
  - Checked before modifying (UPDATE/DELETE)

- **WITH CHECK**: "Can you create/modify to these values?"
  - Checked when inserting (INSERT)
  - Checked after modifying (UPDATE)

**Example:**
```sql
-- User tries to update their profile
UPDATE profiles 
SET full_name = 'John Doe' 
WHERE user_id = 'abc-123';

-- Postgres checks:
1. USING: Is auth.uid() = 'abc-123'? ✅ Yes, proceed
2. WITH CHECK: After update, is auth.uid() still = user_id? ✅ Yes, allow
```

Without WITH CHECK, step 2 fails → RLS violation.

---

## 🔐 Storage Policies Explained

### Current Issue
Storage policies for avatars folder are missing or incorrect.

### Required Policies

1. **Upload Policy:**
```sql
CREATE POLICY "Users can upload avatars"
  ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'documents' AND
    (storage.foldername(name))[1] = 'avatars'
  );
```

2. **View Policy:**
```sql
CREATE POLICY "Anyone can view avatars"
  ON storage.objects
  FOR SELECT
  USING (
    bucket_id = 'documents' AND
    (storage.foldername(name))[1] = 'avatars'
  );
```

### Why Avatars Need Special Treatment
- Profile pictures need to be publicly viewable
- Other documents should be private (user-specific)
- Solution: Separate folder with different policies

---

## 🎯 Verification Commands

### Check if tables exist:
```sql
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('vat_applications', 'profiles');
```

### Check if policies exist:
```sql
SELECT tablename, policyname, cmd
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('vat_applications', 'profiles');
```

### Check storage policies:
```sql
SELECT policyname, cmd
FROM pg_policies 
WHERE schemaname = 'storage' 
AND tablename = 'objects';
```

### Test RLS manually:
```sql
-- Set user context
SET request.jwt.claim.sub = 'your-user-id';

-- Try insert
INSERT INTO vat_applications (user_id, ...) VALUES (...);
-- Should succeed if policies are correct
```

---

## 🚀 After Fixes Applied

### What Changes:

**Before:**
```
User Action → Database → RLS Check → ❌ Policy Missing → Error
```

**After:**
```
User Action → Database → RLS Check → ✅ Policy Exists → Success
```

### Expected Behavior:

1. **Profile Upload:**
   - File uploads to storage/documents/avatars/
   - Profile record updates with avatar_url
   - ✅ Success toast shown

2. **Application Submit:**
   - New row inserted into vat_applications
   - Row has user_id = current user
   - ✅ Success toast shown

3. **Forecast Load:**
   - Edge Function receives request
   - Queries user's VAT documents
   - Returns personalized forecast
   - ✅ Chart displays data

4. **Excel Export:**
   - XLSX library generates workbook
   - Browser downloads .xlsx file
   - ✅ File opens in Excel

---

## 📝 Summary

All 5 errors stem from 3 root causes:
1. **RLS policies incomplete** → 3 errors
2. **Edge Function not deployed** → 1 error
3. **Browser cache stale** → 1 error

**Single fix for each:**
1. Run SQL script → Fixes RLS
2. Deploy function → Fixes forecast
3. Hard refresh → Fixes Excel

**Total time: 5 minutes**
**Total errors fixed: 5**

✅ **All issues resolved!**
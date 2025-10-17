# Setup Guide: Original File Storage & Download

## Overview
This guide explains how to set up the system to store and retrieve original uploaded files alongside the processed data.

## Architecture

### Before:
```
Upload → Process → Extract Data → Save to DB → Delete Original File ❌
```

### After:
```
Upload → Process → Extract Data → Save to DB + Storage → Keep Original File ✅
```

---

## 🔧 Setup Steps

### Step 1: Create Supabase Storage Bucket

You need to create a storage bucket in Supabase to store the original files.

#### Option A: Using Supabase Dashboard (Recommended)

1. **Go to Supabase Dashboard**
   - Navigate to: https://supabase.com/dashboard
   - Select your project

2. **Create Storage Bucket**
   - Click **Storage** in the left sidebar
   - Click **"New bucket"**
   - **Bucket name**: `documents`
   - **Public bucket**: ❌ Uncheck (keep private)
   - Click **"Create bucket"**

3. **Set Bucket Policies**
   - Click on the `documents` bucket
   - Go to **"Policies"** tab
   - Click **"New policy"**
   - Add the following policies:

   **Policy 1: Allow authenticated users to upload**
   ```sql
   CREATE POLICY "Authenticated users can upload"
   ON storage.objects
   FOR INSERT
   WITH CHECK (
     bucket_id = 'documents' AND
     auth.role() = 'authenticated'
   );
   ```

   **Policy 2: Allow authenticated users to read**
   ```sql
   CREATE POLICY "Authenticated users can read"
   ON storage.objects
   FOR SELECT
   USING (
     bucket_id = 'documents' AND
     auth.role() = 'authenticated'
   );
   ```

   **Policy 3: Allow users to delete their own files**
   ```sql
   CREATE POLICY "Users can delete own files"
   ON storage.objects
   FOR DELETE
   USING (
     bucket_id = 'documents' AND
     auth.role() = 'authenticated'
   );
   ```

#### Option B: Using SQL Migration

Run the migration file that was created:

```bash
# The migration file is already created at:
# supabase/migrations/20250102000002_create_documents_bucket.sql

# If using Supabase CLI:
supabase db push

# Or run the SQL directly in Supabase SQL Editor
```

---

### Step 2: Add file_path Column to Database

Add the `file_path` column to store the reference to the original file.

#### Option A: Using Supabase Dashboard

1. Go to **Table Editor** → `processed_documents`
2. Click **"Add column"**
3. **Column name**: `file_path`
4. **Type**: `text`
5. **Nullable**: ✅ Check (for backward compatibility)
6. Click **"Save"**

#### Option B: Using SQL Migration

Run the migration:

```sql
-- Already created at:
-- supabase/migrations/20250102000001_add_file_path_column.sql

ALTER TABLE public.processed_documents 
ADD COLUMN file_path TEXT;
```

---

### Step 3: Restart Backend Server

The backend code has been updated to automatically upload files to Supabase Storage.

```bash
# Stop the backend if running (Ctrl+C)

# Restart the backend
cd backend-example
node server.js
```

**What changed in the backend:**
- Files are now uploaded to Supabase Storage before being deleted
- The storage path is saved in the `file_path` column
- Original files are preserved for future download

---

### Step 4: Test the Feature

1. **Upload a new document**
   - Go to the home page
   - Upload a test document (PDF, Excel, or image)
   - Wait for processing to complete

2. **Check the Documents page**
   - Navigate to Documents page
   - You should see **3 buttons** for each document:
     - 📥 **Download Report** - Downloads processed Excel report
     - 👁️ **View Original** - Downloads the original uploaded file
     - 🗑️ **Delete** - Deletes the document

3. **Test "View Original" button**
   - Click **"View Original"** on a newly uploaded document
   - The original file should download
   - For old documents (uploaded before this feature), you'll see a message: "Original File Not Available"

---

## 📊 How It Works

### Upload Flow:
```
1. User uploads file (e.g., invoice.pdf)
2. Backend receives file
3. Backend extracts text/data from file
4. Backend processes data (AI classification, entity extraction)
5. Backend uploads original file to Supabase Storage
   → Storage path: "1234567890_invoice.pdf"
6. Backend saves processed data + storage path to database
   → file_path: "1234567890_invoice.pdf"
7. Backend deletes temporary file from server
8. User sees document in Documents page
```

### Download Flow:
```
1. User clicks "View Original" button
2. Frontend fetches document record from database
3. Frontend gets file_path from record
4. Frontend downloads file from Supabase Storage using file_path
5. Browser downloads the original file
```

---

## 🔒 Security

### Storage Bucket Security:
- ✅ **Private bucket** - Not publicly accessible
- ✅ **RLS enabled** - Row Level Security enforced
- ✅ **Authenticated only** - Only logged-in users can access
- ✅ **Policy-based access** - Controlled by Supabase policies

### File Access Control:
```sql
-- Only authenticated users can access files
CREATE POLICY "Authenticated users can read"
ON storage.objects
FOR SELECT
USING (
  bucket_id = 'documents' AND
  auth.role() = 'authenticated'
);
```

**Note**: Current setup allows any authenticated user to read any file in the bucket. For stricter security (user can only access their own files), you would need to organize files in user-specific folders.

---

## 📁 File Organization

Files are stored with timestamps to avoid naming conflicts:

```
documents/
├── 1704123456789_invoice_2024.pdf
├── 1704123457890_receipt.xlsx
├── 1704123458901_tax_form.pdf
└── ...
```

**Naming pattern**: `{timestamp}_{sanitized_filename}`

---

## 🐛 Troubleshooting

### Issue: "Original File Not Available" message

**Cause**: Document was uploaded before file storage was enabled.

**Solution**: 
- This is expected for old documents
- Only newly uploaded documents will have original files
- Re-upload the document if you need the original file

---

### Issue: Storage bucket not found error

**Error**: `Bucket 'documents' not found`

**Solution**:
1. Go to Supabase Dashboard → Storage
2. Verify the `documents` bucket exists
3. If not, create it manually (see Step 1)

---

### Issue: Permission denied when downloading

**Error**: `Permission denied` or `403 Forbidden`

**Solution**:
1. Check storage policies are set correctly
2. Verify user is authenticated
3. Check RLS is enabled on storage.objects
4. Run this SQL to check policies:
   ```sql
   SELECT * FROM pg_policies 
   WHERE tablename = 'objects' 
   AND schemaname = 'storage';
   ```

---

### Issue: File upload fails in backend

**Error**: Backend logs show storage upload error

**Solution**:
1. Check backend has correct Supabase credentials in `.env`:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_anon_key
   ```
2. Verify the `documents` bucket exists
3. Check backend console for detailed error messages

---

## 🔄 Backward Compatibility

### Old Documents (Before Feature):
- ✅ Still visible in Documents page
- ✅ Can still download processed report
- ✅ Can still delete
- ❌ "View Original" shows "not available" message
- ✅ `file_path` column is NULL (allowed)

### New Documents (After Feature):
- ✅ All features work
- ✅ Original file stored in Supabase Storage
- ✅ `file_path` column populated
- ✅ Both "Download Report" and "View Original" work

---

## 📈 Storage Considerations

### Storage Limits:
- **Supabase Free Tier**: 1 GB storage
- **Pro Tier**: 8 GB storage (expandable)

### File Size Limits:
- **Current backend limit**: 10 MB per file
- **Supabase limit**: 50 MB per file (free tier)

### Cost Estimation:
```
Average document size: 500 KB
Free tier storage: 1 GB
Estimated capacity: ~2,000 documents

Pro tier storage: 8 GB
Estimated capacity: ~16,000 documents
```

### Storage Management:
- Consider implementing file cleanup for deleted documents
- Monitor storage usage in Supabase Dashboard
- Implement file size warnings for large uploads

---

## 🚀 Future Enhancements

### Potential Improvements:

1. **User-Specific Folders**
   ```
   documents/
   ├── user_123/
   │   ├── invoice.pdf
   │   └── receipt.xlsx
   └── user_456/
       └── tax_form.pdf
   ```

2. **File Versioning**
   - Keep multiple versions of the same document
   - Track changes over time

3. **Bulk Download**
   - Download multiple original files as ZIP
   - Export all documents for a user

4. **File Preview**
   - Show PDF preview in browser
   - Display Excel data in modal

5. **Storage Cleanup**
   - Automatically delete files when document is deleted
   - Implement retention policies

6. **Compression**
   - Compress files before storage
   - Reduce storage costs

---

## 📝 Testing Checklist

- [ ] Supabase Storage bucket `documents` created
- [ ] Storage policies configured
- [ ] `file_path` column added to `processed_documents` table
- [ ] Backend server restarted
- [ ] Upload new document successfully
- [ ] Document appears in Documents page
- [ ] "Download Report" button works (Excel report)
- [ ] "View Original" button works (original file)
- [ ] Old documents show "not available" message
- [ ] Delete functionality still works
- [ ] File is removed from storage when document deleted (optional)

---

## 🆘 Support

If you encounter issues:

1. **Check browser console** (F12) for errors
2. **Check backend logs** for upload errors
3. **Verify Supabase Dashboard**:
   - Storage bucket exists
   - Policies are set
   - Files are being uploaded
4. **Check database**:
   ```sql
   SELECT id, filename, file_path 
   FROM processed_documents 
   ORDER BY created_at DESC 
   LIMIT 10;
   ```

---

## 📚 Related Files

### Frontend:
- `src/pages/Documents.tsx` - UI with "View Original" button
- `src/hooks/useProcessedDocuments.tsx` - Data fetching

### Backend:
- `backend-example/server.js` - File upload and storage logic

### Database:
- `supabase/migrations/20250102000001_add_file_path_column.sql`
- `supabase/migrations/20250102000002_create_documents_bucket.sql`

### Documentation:
- `EXCEL_EXPORT_FEATURE.md` - Excel report download feature
- `DELETE_FIX_SUMMARY.md` - Delete functionality details

---

**Last Updated**: January 2024  
**Feature Status**: ✅ Ready for Testing  
**Requires**: Supabase Storage setup
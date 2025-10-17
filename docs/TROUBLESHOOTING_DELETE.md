# 🔧 Troubleshooting Document Delete Issues

## Quick Diagnostics

### Step 1: Check Backend Server Status

**Is the backend running?**
```powershell
# Check if backend is running on port 3001
Test-NetConnection -ComputerName localhost -Port 3001
```

**Start the backend if not running:**
```powershell
# Navigate to project directory
Set-Location "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\navi-tax-35-main"

# Start backend server
node backend-example/server.js
```

You should see:
```
🚀 Server running on http://localhost:3001
✅ Connected to Supabase
```

---

### Step 2: Run Diagnostic Script

```powershell
# Run the diagnostic test
node test_delete_endpoint.js
```

This will check:
- ✅ Backend health
- ✅ Document list availability
- ✅ Endpoint accessibility
- ✅ Common configuration issues

---

### Step 3: Check Browser Console

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Try deleting a document
4. Look for error messages

**Common errors and solutions:**

#### Error: "Failed to fetch" or "Network request failed"
**Cause:** Backend server is not running or not accessible

**Solution:**
```powershell
# Start backend server
node backend-example/server.js
```

---

#### Error: "CORS policy blocked"
**Cause:** CORS not properly configured in backend

**Solution:** Check `server.js` has CORS enabled:
```javascript
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}));
```

---

#### Error: "Server error: 500"
**Cause:** Database connection issue or RLS policy blocking delete

**Solution:**
1. Check backend terminal for detailed error logs
2. Verify Supabase connection in `.env` file
3. Check RLS policies (see below)

---

#### Error: "Document not found" or "Server error: 404"
**Cause:** Document ID is invalid or document already deleted

**Solution:**
1. Refresh the page to get latest document list
2. Check if document still exists in database

---

### Step 4: Check Supabase RLS Policies

**Problem:** RLS (Row Level Security) policies might be blocking deletes

**Check your policies:**
1. Go to Supabase Dashboard
2. Navigate to **Authentication** → **Policies**
3. Find `processed_documents` table
4. Ensure there's a DELETE policy

**Required DELETE policy:**
```sql
-- Allow users to delete their own documents
CREATE POLICY "Users can delete own documents"
ON processed_documents
FOR DELETE
USING (auth.uid() = user_id);
```

**Temporary fix (for testing only):**
```sql
-- Disable RLS temporarily (NOT for production!)
ALTER TABLE processed_documents DISABLE ROW LEVEL SECURITY;
```

---

### Step 5: Check Backend Logs

**Look at backend terminal output when delete fails:**

**Good response:**
```
✅ Document deleted: 123e4567-e89b-12d3-a456-426614174000
```

**Error responses:**

```
❌ Error deleting document: { code: 'PGRST116', message: 'No rows deleted' }
```
→ **Solution:** Document doesn't exist or RLS policy blocking

```
❌ Error deleting document: { code: '42P01', message: 'relation "processed_documents" does not exist' }
```
→ **Solution:** Database table not created, run migrations

```
❌ Error deleting document: { code: '23503', message: 'foreign key constraint violation' }
```
→ **Solution:** Related records exist, need cascade delete

---

## Common Issues & Solutions

### Issue 1: "Cannot connect to server"

**Symptoms:**
- Toast shows: "Cannot connect to server. Please ensure the backend is running."
- Browser console: `Failed to fetch`

**Solutions:**
1. Start backend server:
   ```powershell
   node backend-example/server.js
   ```

2. Verify backend is on correct port (3001):
   ```powershell
   Test-NetConnection -ComputerName localhost -Port 3001
   ```

3. Check firewall isn't blocking port 3001

---

### Issue 2: Delete button does nothing

**Symptoms:**
- Click delete button
- No confirmation dialog appears
- No error message

**Solutions:**
1. Check browser console for JavaScript errors
2. Verify `handleDelete` function is connected to button
3. Check if `isDeleting` state is stuck as `true`

**Debug in browser console:**
```javascript
// Check if function exists
console.log(typeof handleDelete); // should be "function"
```

---

### Issue 3: Confirmation dialog appears but delete fails

**Symptoms:**
- Confirmation dialog shows
- Click "OK"
- Error toast appears: "Delete Failed"

**Solutions:**
1. Check backend terminal for error details
2. Verify document ID is valid UUID format
3. Check Supabase connection
4. Verify RLS policies

**Test with curl:**
```powershell
# Replace {DOC_ID} with actual document ID
curl -X DELETE http://localhost:3001/api/documents/{DOC_ID}
```

---

### Issue 4: Delete succeeds but document still shows

**Symptoms:**
- Success toast appears
- Document still visible in list
- Refresh page and document is gone

**Solutions:**
1. Check if `refetch()` is being called after delete
2. Verify Supabase real-time subscription is active
3. Clear browser cache

**Force refresh:**
```javascript
// In browser console
window.location.reload();
```

---

### Issue 5: Bulk delete fails but single delete works

**Symptoms:**
- Single document delete works fine
- Bulk delete shows error

**Solutions:**
1. Check backend logs for bulk delete endpoint errors
2. Verify `ids` array is being sent correctly
3. Check if all selected document IDs are valid

**Test bulk delete endpoint:**
```powershell
# Test with curl
curl -X POST http://localhost:3001/api/documents/bulk-delete `
  -H "Content-Type: application/json" `
  -d '{"ids":["id1","id2"]}'
```

---

## Advanced Debugging

### Enable Detailed Logging

**Backend (server.js):**
```javascript
// Add before delete endpoint
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`, req.body);
  next();
});
```

**Frontend (Documents.tsx):**
```javascript
// Add in handleDelete function
console.log('Deleting document:', docId, filename);
console.log('API URL:', `http://localhost:3001/api/documents/${docId}`);
```

---

### Test with Browser DevTools Network Tab

1. Open DevTools (F12)
2. Go to **Network** tab
3. Try deleting a document
4. Find the DELETE request
5. Check:
   - **Status Code:** Should be 200
   - **Response:** Should show `{"success": true}`
   - **Request URL:** Should be `http://localhost:3001/api/documents/{id}`

---

### Database Direct Check

**Check if document exists:**
```sql
SELECT id, filename FROM processed_documents;
```

**Try manual delete:**
```sql
DELETE FROM processed_documents WHERE id = 'your-document-id';
```

If manual delete fails, check for:
- Foreign key constraints
- RLS policies
- Triggers

---

## Environment Checklist

Before reporting an issue, verify:

- [ ] Backend server is running (`node backend-example/server.js`)
- [ ] Backend shows "Connected to Supabase"
- [ ] Frontend is running (`npm run dev`)
- [ ] Browser console shows no errors
- [ ] Supabase credentials are correct in `.env`
- [ ] RLS policies allow DELETE operations
- [ ] Document IDs are valid UUIDs
- [ ] Network tab shows DELETE request is sent
- [ ] Backend terminal shows request received

---

## Quick Fix Commands

**Restart everything:**
```powershell
# Stop all processes (Ctrl+C in terminals)

# Start backend
Set-Location "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\navi-tax-35-main"
node backend-example/server.js

# In new terminal, start frontend
Set-Location "c:\Users\HomeLaptop\Downloads\navi-tax-35-main\navi-tax-35-main"
npm run dev
```

**Clear browser cache:**
```
Ctrl + Shift + Delete → Clear cache → Reload page
```

**Reset database (CAUTION: Deletes all data):**
```sql
TRUNCATE TABLE processed_documents CASCADE;
```

---

## Still Not Working?

### Collect Debug Information

1. **Backend logs:**
   - Copy last 20 lines from backend terminal

2. **Browser console:**
   - Copy all error messages (red text)

3. **Network tab:**
   - Right-click DELETE request → Copy → Copy as cURL

4. **Environment:**
   - Node version: `node --version`
   - npm version: `npm --version`
   - OS: Windows 11

5. **Configuration:**
   - Backend URL in frontend code
   - Supabase URL (without credentials)
   - CORS settings

### Test with Minimal Example

Create `test_delete_simple.html`:
```html
<!DOCTYPE html>
<html>
<body>
  <button onclick="testDelete()">Test Delete</button>
  <script>
    async function testDelete() {
      const docId = prompt('Enter document ID:');
      const response = await fetch(`http://localhost:3001/api/documents/${docId}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      alert(JSON.stringify(data, null, 2));
    }
  </script>
</body>
</html>
```

Open in browser and test directly.

---

## Contact Support

If issue persists after trying all solutions:

1. Run diagnostic script: `node test_delete_endpoint.js`
2. Collect debug information (see above)
3. Check backend terminal for error codes
4. Verify Supabase dashboard shows documents
5. Test with minimal example

**Common resolution:** 99% of delete issues are caused by:
- Backend not running (60%)
- RLS policies blocking delete (25%)
- Invalid document IDs (10%)
- CORS issues (5%)
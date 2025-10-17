# Document Download & Delete Functionality Implementation

## 📋 Overview

This document describes the implementation of **download** and **delete** functionality for the Documents page, including **multi-select** capabilities for bulk deletion.

---

## ✅ Features Implemented

### 1. **Single Document Download** 📥
- Click the "Download" button on any document card
- Downloads a JSON report containing:
  - Document metadata (filename, type, classification, confidence)
  - All extracted entities (GST numbers, amounts, dates, etc.)
  - Processing timestamps
- File format: `{original_filename}_report.json`

### 2. **Single Document Delete** 🗑️
- Click the "Delete" button on any document card
- Confirmation dialog before deletion
- Real-time UI update after deletion
- Toast notification for success/failure

### 3. **Multi-Select Functionality** ☑️
- Checkbox on each document card for selection
- Visual feedback: Selected cards have blue ring and background tint
- "Select All" / "Deselect All" button in toolbar
- Selection counter badge showing number of selected documents

### 4. **Bulk Delete** 🗑️✖️
- Delete multiple documents at once
- Bulk action toolbar appears when documents are available
- "Delete X Document(s)" button in toolbar
- Confirmation dialog before bulk deletion
- Efficient single API call for multiple deletions

---

## 🔧 Technical Implementation

### Backend Changes (`backend-example/server.js`)

#### **1. Delete Single Document Endpoint**
```javascript
DELETE /api/documents/:id
```
- Deletes a document by ID from Supabase
- Returns success/error response
- Respects RLS (Row Level Security) policies

#### **2. Bulk Delete Endpoint**
```javascript
POST /api/documents/bulk-delete
Body: { ids: ["uuid1", "uuid2", ...] }
```
- Accepts array of document IDs
- Deletes all specified documents in one database operation
- Returns count of deleted documents

#### **3. Download Document Endpoint**
```javascript
GET /api/documents/:id/download
```
- Fetches document data from Supabase
- Returns formatted JSON with all document information
- Sets proper headers for file download
- Filename format: `{original_name}_report.json`

---

### Frontend Changes (`src/pages/Documents.tsx`)

#### **New State Variables**
```typescript
const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
const [isDeleting, setIsDeleting] = useState(false);
const { toast } = useToast();
```

#### **New Functions**

1. **`toggleDocumentSelection(docId: string)`**
   - Toggles selection state for a single document
   - Updates `selectedDocuments` array

2. **`selectAllDocuments()`**
   - Selects/deselects all filtered documents
   - Smart toggle based on current selection state

3. **`handleDownload(docId: string, filename: string)`**
   - Fetches document data from backend
   - Creates blob and triggers browser download
   - Shows success/error toast notification

4. **`handleDelete(docId: string, filename: string)`**
   - Shows confirmation dialog
   - Calls DELETE endpoint
   - Refreshes document list via `refetch()`
   - Shows toast notification

5. **`handleBulkDelete()`**
   - Validates selection (at least 1 document)
   - Shows confirmation with count
   - Calls bulk delete endpoint
   - Clears selection and refreshes list
   - Shows toast notification

#### **UI Components Added**

1. **Bulk Actions Toolbar**
   ```tsx
   <Card className="bg-muted/50">
     - "Select All" / "Deselect All" button
     - Selection counter badge
     - "Delete X Document(s)" button (when items selected)
   </Card>
   ```

2. **Document Card Checkbox**
   ```tsx
   <button onClick={() => toggleDocumentSelection(doc.id)}>
     {selected ? <CheckSquare /> : <Square />}
   </button>
   ```

3. **Visual Selection Feedback**
   ```tsx
   className={`hover:shadow-lg transition-all ${
     selectedDocuments.includes(doc.id) 
       ? 'ring-2 ring-intelligence-blue bg-intelligence-blue/5' 
       : ''
   }`}
   ```

4. **Connected Action Buttons**
   ```tsx
   <Button onClick={() => handleDownload(doc.id, doc.filename)}>
     Download
   </Button>
   <Button onClick={() => handleDelete(doc.id, doc.filename)}>
     Delete
   </Button>
   ```

---

## 🎨 User Experience Flow

### **Download Flow**
1. User clicks "Download" button on document card
2. Frontend fetches document data from backend
3. JSON blob is created with formatted data
4. Browser triggers download with filename `{original}_report.json`
5. Success toast appears: "Download Successful"

### **Single Delete Flow**
1. User clicks "Delete" button on document card
2. Confirmation dialog: "Are you sure you want to delete '{filename}'?"
3. If confirmed, DELETE request sent to backend
4. Document removed from Supabase database
5. UI refreshes automatically (via `refetch()`)
6. Success toast appears: "Document Deleted"

### **Multi-Select & Bulk Delete Flow**
1. User clicks checkboxes on multiple document cards
2. Selected cards show blue ring and background tint
3. Toolbar shows selection count: "3 selected"
4. User clicks "Delete 3 Document(s)" button
5. Confirmation dialog: "Are you sure you want to delete 3 document(s)?"
6. If confirmed, bulk delete request sent with array of IDs
7. All selected documents removed from database
8. Selection cleared, UI refreshes
9. Success toast: "3 document(s) deleted successfully"

---

## 🔒 Security Considerations

### **Row Level Security (RLS)**
- All database operations respect Supabase RLS policies
- Users can only delete their own documents
- Policy: `auth.uid() = user_id OR user_id IS NULL`

### **Input Validation**
- Backend validates document IDs (UUID format)
- Bulk delete validates array of IDs
- Empty selections prevented on frontend

### **Error Handling**
- Try-catch blocks on all async operations
- User-friendly error messages via toast notifications
- Console logging for debugging
- Graceful degradation on failures

---

## 📊 API Endpoints Summary

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| `DELETE` | `/api/documents/:id` | Delete single document | None | `{ success, message }` |
| `POST` | `/api/documents/bulk-delete` | Delete multiple documents | `{ ids: string[] }` | `{ success, message, count }` |
| `GET` | `/api/documents/:id/download` | Download document report | None | JSON file download |

---

## 🧪 Testing Checklist

### **Download Functionality**
- ✅ Click download button on a document
- ✅ Verify JSON file downloads with correct filename
- ✅ Check JSON contains all document data (entities, metadata)
- ✅ Verify toast notification appears

### **Single Delete Functionality**
- ✅ Click delete button on a document
- ✅ Verify confirmation dialog appears
- ✅ Cancel deletion and verify document remains
- ✅ Confirm deletion and verify document disappears
- ✅ Verify toast notification appears
- ✅ Refresh page and verify document is gone

### **Multi-Select Functionality**
- ✅ Click checkbox on a document - verify selection
- ✅ Click checkbox again - verify deselection
- ✅ Click "Select All" - verify all documents selected
- ✅ Click "Deselect All" - verify all deselected
- ✅ Verify selection counter updates correctly
- ✅ Verify selected cards have visual feedback (blue ring)

### **Bulk Delete Functionality**
- ✅ Select multiple documents (e.g., 3 documents)
- ✅ Verify toolbar shows "3 selected"
- ✅ Click "Delete 3 Document(s)" button
- ✅ Verify confirmation dialog shows correct count
- ✅ Cancel and verify documents remain
- ✅ Confirm and verify all selected documents disappear
- ✅ Verify selection is cleared after deletion
- ✅ Verify toast shows correct count
- ✅ Refresh page and verify documents are gone

### **Edge Cases**
- ✅ Try to bulk delete with 0 selections - verify error toast
- ✅ Delete all documents - verify empty state appears
- ✅ Search and select filtered documents - verify only filtered ones selected
- ✅ Delete while another delete is in progress - verify button disabled

---

## 🚀 How to Use

### **For Users**

#### **Download a Document Report:**
1. Navigate to Documents page (`/documents`)
2. Find the document you want to download
3. Click the "Download" button on the right side
4. JSON report will download to your browser's download folder

#### **Delete a Single Document:**
1. Navigate to Documents page
2. Find the document you want to delete
3. Click the "Delete" button (red text)
4. Confirm the deletion in the dialog
5. Document will be removed immediately

#### **Delete Multiple Documents:**
1. Navigate to Documents page
2. Click the checkbox on each document you want to delete
3. Selected documents will have a blue ring
4. Click "Delete X Document(s)" button in the toolbar
5. Confirm the bulk deletion
6. All selected documents will be removed

#### **Select/Deselect All:**
1. Click "Select All" button in toolbar to select all visible documents
2. Click "Deselect All" to clear all selections

---

## 📁 Files Modified

### **Backend**
- ✅ `backend-example/server.js` - Added 3 new endpoints (delete, bulk-delete, download)

### **Frontend**
- ✅ `src/pages/Documents.tsx` - Added multi-select UI, handlers, and action buttons

### **No New Files Created**
All functionality added to existing files.

---

## 🔄 Real-Time Updates

The Documents page uses **Supabase real-time subscriptions** (already implemented in `useProcessedDocuments` hook):
- When a document is deleted, the subscription detects the change
- The document list automatically refreshes
- No manual page refresh needed
- Works across multiple browser tabs/windows

---

## 🎯 Future Enhancements (Optional)

### **Potential Improvements:**
1. **Download Original Files**: Store and serve original uploaded files (PDF/Excel)
2. **Export Formats**: Add CSV, Excel, or PDF export options
3. **Bulk Download**: Download multiple documents as a ZIP file
4. **Undo Delete**: Soft delete with recovery option
5. **Drag & Drop Selection**: Select multiple documents by dragging
6. **Keyboard Shortcuts**: Ctrl+A for select all, Delete key for deletion
7. **Sorting & Filtering**: Sort by date, type, classification before bulk actions
8. **Preview Before Download**: Show document preview in modal
9. **Share Documents**: Generate shareable links for documents
10. **Document Versioning**: Track changes and maintain version history

---

## 🐛 Troubleshooting

### **Download Not Working**
- Check browser console for errors
- Verify backend is running on `http://localhost:3001`
- Check CORS settings in `server.js`
- Verify document ID exists in database

### **Delete Not Working**
- Check if backend server is running
- Verify Supabase connection
- Check RLS policies allow deletion
- Look for errors in browser console and backend logs

### **Bulk Delete Not Working**
- Ensure at least one document is selected
- Check network tab for API request/response
- Verify IDs array is being sent correctly
- Check backend logs for database errors

### **Selection Not Persisting**
- Selection is intentionally cleared after bulk delete
- Selection is local state (not persisted across page refreshes)
- This is expected behavior for better UX

---

## 📞 Support

If you encounter issues:
1. Check browser console for JavaScript errors
2. Check backend terminal for server errors
3. Verify Supabase connection and RLS policies
4. Test API endpoints directly using Postman/curl
5. Check network tab in browser DevTools

---

## ✨ Summary

**What Was Added:**
- ✅ Download button functionality (JSON reports)
- ✅ Delete button functionality (single documents)
- ✅ Multi-select checkboxes on document cards
- ✅ Bulk action toolbar with select all/deselect all
- ✅ Bulk delete functionality (multiple documents at once)
- ✅ Visual feedback for selected documents
- ✅ Toast notifications for all actions
- ✅ Confirmation dialogs for destructive actions
- ✅ Real-time UI updates after operations
- ✅ Backend API endpoints for all operations

**User Benefits:**
- 🎯 Quickly download document reports for record-keeping
- 🗑️ Easily remove unwanted documents
- ⚡ Efficiently delete multiple documents at once
- 👁️ Clear visual feedback for selections
- 🔔 Instant notifications for action results
- 🔒 Safe operations with confirmation dialogs

---

**Implementation Date:** January 2025  
**Status:** ✅ Fully Operational  
**Backend Server Required:** Yes (`http://localhost:3001`)
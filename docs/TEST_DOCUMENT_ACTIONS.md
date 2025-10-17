# Quick Test Guide - Document Actions

## 🚀 Quick Start

### **Prerequisites**
1. ✅ Backend server running on `http://localhost:3001`
2. ✅ Frontend running on `http://localhost:8080`
3. ✅ At least 3-5 documents uploaded to test with

---

## 🧪 Test Scenarios

### **Test 1: Download Single Document** ⬇️

**Steps:**
1. Navigate to `/documents` page
2. Find any document in the list
3. Click the **"Download"** button on the right side
4. Check your browser's download folder

**Expected Results:**
- ✅ JSON file downloads with name: `{filename}_report.json`
- ✅ Toast notification appears: "Download Successful"
- ✅ File contains document metadata and entities

**Sample Downloaded File:**
```json
{
  "filename": "tax_invoice_2024.xlsx",
  "type": "Tax Invoice",
  "classification": "Compliant",
  "confidence": 0.875,
  "processed_at": "2025-01-15T10:30:00Z",
  "entities": [
    "GST: GSTIN36098059",
    "Amount: 1,4,166.00",
    "Date: 2025-04-10",
    ...
  ],
  "metadata": {
    "id": "uuid-here",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

---

### **Test 2: Delete Single Document** 🗑️

**Steps:**
1. Navigate to `/documents` page
2. Find a document you want to delete
3. Click the **"Delete"** button (red text)
4. Confirm deletion in the dialog

**Expected Results:**
- ✅ Confirmation dialog appears with document name
- ✅ After confirming, document disappears from list
- ✅ Toast notification: "Document Deleted"
- ✅ Document count in header decreases by 1
- ✅ Refresh page - document is still gone (persisted)

---

### **Test 3: Select/Deselect Documents** ☑️

**Steps:**
1. Navigate to `/documents` page
2. Click the checkbox on the left of a document card
3. Click the checkbox again to deselect
4. Click checkboxes on 3 different documents

**Expected Results:**
- ✅ Clicking checkbox selects document (blue ring appears)
- ✅ Clicking again deselects (blue ring disappears)
- ✅ Selection counter updates: "3 selected"
- ✅ Bulk delete button appears in toolbar

---

### **Test 4: Select All / Deselect All** ☑️✖️

**Steps:**
1. Navigate to `/documents` page
2. Click **"Select All"** button in toolbar
3. Verify all documents are selected
4. Click **"Deselect All"** button
5. Verify all documents are deselected

**Expected Results:**
- ✅ "Select All" selects all visible documents
- ✅ All cards show blue ring and background tint
- ✅ Button text changes to "Deselect All"
- ✅ Selection counter shows total count
- ✅ "Deselect All" clears all selections

---

### **Test 5: Bulk Delete** 🗑️✖️

**Steps:**
1. Navigate to `/documents` page
2. Select 3 documents using checkboxes
3. Click **"Delete 3 Document(s)"** button in toolbar
4. Confirm deletion in dialog

**Expected Results:**
- ✅ Confirmation dialog shows correct count: "3 document(s)"
- ✅ After confirming, all 3 documents disappear
- ✅ Toast notification: "3 document(s) deleted successfully"
- ✅ Selection is cleared automatically
- ✅ Document count in header decreases by 3
- ✅ Refresh page - documents are still gone

---

### **Test 6: Search and Select** 🔍☑️

**Steps:**
1. Navigate to `/documents` page
2. Type "invoice" in the search bar
3. Click **"Select All"** button
4. Verify only filtered documents are selected

**Expected Results:**
- ✅ Only documents matching "invoice" are shown
- ✅ "Select All" selects only visible (filtered) documents
- ✅ Selection counter shows count of filtered documents
- ✅ Can bulk delete only the filtered selection

---

### **Test 7: Cancel Operations** ❌

**Steps:**
1. Click "Delete" on a document
2. Click "Cancel" in confirmation dialog
3. Select 3 documents
4. Click "Delete 3 Document(s)"
5. Click "Cancel" in confirmation dialog

**Expected Results:**
- ✅ Document is NOT deleted after canceling
- ✅ Documents remain in list
- ✅ Selection remains intact
- ✅ No toast notification appears

---

### **Test 8: Error Handling** ⚠️

**Steps:**
1. Stop the backend server
2. Try to download a document
3. Try to delete a document
4. Restart backend and try again

**Expected Results:**
- ✅ Error toast appears: "Download Failed"
- ✅ Error toast appears: "Delete Failed"
- ✅ Documents remain in list (no data loss)
- ✅ After restarting backend, operations work again

---

### **Test 9: Empty Selection Bulk Delete** 🚫

**Steps:**
1. Navigate to `/documents` page
2. Ensure no documents are selected
3. Try to click bulk delete button (should not be visible)

**Expected Results:**
- ✅ Bulk delete button is NOT visible when nothing is selected
- ✅ Only "Select All" button is visible

---

### **Test 10: Real-Time Updates** 🔄

**Steps:**
1. Open `/documents` page in two browser tabs
2. In Tab 1, delete a document
3. Watch Tab 2 (don't refresh)

**Expected Results:**
- ✅ Tab 2 automatically updates (document disappears)
- ✅ No manual refresh needed
- ✅ Real-time subscription working

---

## 🎯 Visual Verification Checklist

### **Checkboxes**
- [ ] Empty square (☐) when unselected
- [ ] Filled checkmark (☑️) when selected
- [ ] Hover effect on checkboxes
- [ ] Smooth transition between states

### **Selected Cards**
- [ ] Blue ring (2px) around card
- [ ] Light blue background tint
- [ ] Smooth animation when selecting
- [ ] Smooth animation when deselecting

### **Toolbar**
- [ ] "Select All" button visible when documents exist
- [ ] Button text toggles: "Select All" ↔ "Deselect All"
- [ ] Selection counter badge appears when > 0 selected
- [ ] Bulk delete button appears only when items selected
- [ ] Bulk delete button shows correct count

### **Action Buttons**
- [ ] Download button has download icon
- [ ] Delete button has trash icon and red text
- [ ] Hover effects on both buttons
- [ ] Disabled state during deletion (gray, not clickable)

### **Toast Notifications**
- [ ] Success toasts are green
- [ ] Error toasts are red
- [ ] Toasts appear in top-right corner
- [ ] Toasts auto-dismiss after 5 seconds
- [ ] Toasts show correct messages

### **Confirmation Dialogs**
- [ ] Dialog appears before deletion
- [ ] Dialog shows document name (single delete)
- [ ] Dialog shows count (bulk delete)
- [ ] "Cancel" and "Delete" buttons present
- [ ] Dialog closes after action

---

## 🐛 Common Issues & Solutions

### **Issue: Download button does nothing**
**Solution:**
- Check browser console for errors
- Verify backend is running: `http://localhost:3001/api/health`
- Check browser's download settings (not blocked)

### **Issue: Delete button doesn't work**
**Solution:**
- Check if backend server is running
- Verify Supabase connection
- Check browser console for errors
- Look at backend terminal for error logs

### **Issue: Bulk delete button not appearing**
**Solution:**
- Ensure at least one document is selected
- Check if toolbar is visible (only shows when documents exist)
- Verify selection state in React DevTools

### **Issue: Selection not working**
**Solution:**
- Check browser console for JavaScript errors
- Verify document IDs are valid UUIDs
- Clear browser cache and reload

### **Issue: Real-time updates not working**
**Solution:**
- Check Supabase connection
- Verify real-time subscription in `useProcessedDocuments` hook
- Check browser console for WebSocket errors

---

## 📊 Performance Testing

### **Test with Large Dataset**
1. Upload 50+ documents
2. Test "Select All" performance
3. Test bulk delete with 20+ documents
4. Verify UI remains responsive

**Expected:**
- ✅ Selection happens instantly
- ✅ Bulk delete completes within 2-3 seconds
- ✅ UI doesn't freeze or lag
- ✅ Smooth animations maintained

---

## 🔒 Security Testing

### **Test RLS (Row Level Security)**
1. Login as User A
2. Upload documents
3. Logout and login as User B
4. Try to access User A's documents

**Expected:**
- ✅ User B cannot see User A's documents
- ✅ User B cannot delete User A's documents
- ✅ API returns 403 or empty results

---

## ✅ Final Checklist

Before marking as complete, verify:

- [ ] Download works for all document types (PDF, Excel, images)
- [ ] Single delete works and persists after refresh
- [ ] Bulk delete works for 1, 3, 5, 10+ documents
- [ ] Select All / Deselect All works correctly
- [ ] Search + Select All selects only filtered documents
- [ ] Confirmation dialogs appear for all delete operations
- [ ] Toast notifications appear for all actions
- [ ] Error handling works when backend is down
- [ ] Real-time updates work across multiple tabs
- [ ] Visual feedback (blue rings, hover effects) works
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] No console errors during normal operation
- [ ] Backend logs show successful operations

---

## 📝 Test Report Template

```
Date: _______________
Tester: _______________

Test Results:
✅ Download Single Document: PASS / FAIL
✅ Delete Single Document: PASS / FAIL
✅ Select/Deselect Documents: PASS / FAIL
✅ Select All / Deselect All: PASS / FAIL
✅ Bulk Delete: PASS / FAIL
✅ Search and Select: PASS / FAIL
✅ Cancel Operations: PASS / FAIL
✅ Error Handling: PASS / FAIL
✅ Empty Selection: PASS / FAIL
✅ Real-Time Updates: PASS / FAIL

Visual Verification:
✅ Checkboxes: PASS / FAIL
✅ Selected Cards: PASS / FAIL
✅ Toolbar: PASS / FAIL
✅ Action Buttons: PASS / FAIL
✅ Toast Notifications: PASS / FAIL
✅ Confirmation Dialogs: PASS / FAIL

Issues Found:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Notes:
_______________________________________________
_______________________________________________
_______________________________________________
```

---

## 🎉 Success Criteria

**All features working correctly when:**
- ✅ All 10 test scenarios pass
- ✅ All visual elements display correctly
- ✅ No console errors during normal operation
- ✅ Backend logs show successful API calls
- ✅ Real-time updates work across tabs
- ✅ Error handling gracefully handles failures
- ✅ Performance is acceptable with 50+ documents

---

**Happy Testing!** 🚀✨
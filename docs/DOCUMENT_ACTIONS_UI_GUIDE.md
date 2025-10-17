# Document Actions - Visual UI Guide

## 🎨 UI Components Overview

### **1. Bulk Actions Toolbar**

```
┌─────────────────────────────────────────────────────────────────────┐
│  📋 Bulk Actions Toolbar (appears when documents exist)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [☐ Select All]  [3 selected]              [🗑️ Delete 3 Document(s)]│
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Features:**
- **Select All Button**: Toggles between "Select All" and "Deselect All"
- **Selection Badge**: Shows count of selected documents (only when > 0)
- **Bulk Delete Button**: Appears only when documents are selected
- **Background**: Muted gray background to distinguish from document cards

---

### **2. Document Card - Unselected State**

```
┌─────────────────────────────────────────────────────────────────────┐
│  ☐  📄 tax_invoice_2024.xlsx                        [⬇️ Download]   │
│      Type: Tax Invoice                              [🗑️ Delete]     │
│                                                                       │
│      [✓ Compliant]  [Confidence: 87.5%]                             │
│                                                                       │
│      📌 Extracted Information:                                       │
│      ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│      │ GST: 34 │  │Amount:156│  │Date: 26 │  │Company:45│           │
│      │GSTIN... │  │1,4,166...│  │2025-04..│  │Sheet +44 │           │
│      └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
│                                                                       │
│      📅 Processed: Jan 15, 2025, 10:30 AM                           │
└─────────────────────────────────────────────────────────────────────┘
```

**Features:**
- **Checkbox**: Empty square on the left
- **File Icon**: Blue document icon
- **Filename**: Bold, large text
- **Type**: Smaller gray text below filename
- **Classification Badge**: Color-coded (green for Compliant)
- **Confidence Badge**: Blue badge with percentage
- **Entity Summary**: Grid of cards showing counts
- **Timestamp**: Gray text with calendar icon
- **Action Buttons**: Download (outline) and Delete (red text)

---

### **3. Document Card - Selected State**

```
┌═════════════════════════════════════════════════════════════════════┐ ← Blue ring
║  ☑️  📄 tax_invoice_2024.xlsx                        [⬇️ Download]   ║
║      Type: Tax Invoice                              [🗑️ Delete]     ║
║                                                                       ║
║      [✓ Compliant]  [Confidence: 87.5%]                             ║
║                                                                       ║
║      📌 Extracted Information:                                       ║
║      ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           ║
║      │ GST: 34 │  │Amount:156│  │Date: 26 │  │Company:45│           ║
║      │GSTIN... │  │1,4,166...│  │2025-04..│  │Sheet +44 │           ║
║      └─────────┘  └─────────┘  └─────────┘  └─────────┘           ║
║                                                                       ║
║      📅 Processed: Jan 15, 2025, 10:30 AM                           ║
╚═════════════════════════════════════════════════════════════════════╝
   ↑ Blue background tint
```

**Visual Changes When Selected:**
- ✅ **Checkbox**: Filled blue checkmark
- 🔵 **Blue Ring**: 2px blue border around entire card
- 🎨 **Background Tint**: Light blue background overlay
- ✨ **Smooth Transition**: Animated state change

---

### **4. Complete Page Layout**

```
┌─────────────────────────────────────────────────────────────────────┐
│  📚 Uploaded Documents                                    [46 Documents]│
│  View and manage all your processed tax documents                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  🔍 Search by filename, type, or classification...          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  [☐ Select All]  [3 selected]    [🗑️ Delete 3 Document(s)] │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌═══════════════════════════════════════════════════════════════┐ │ ← Selected
│  ║  ☑️  📄 tax_invoice_2024.xlsx          [⬇️ Download]         ║ │
│  ║      Type: Tax Invoice                [🗑️ Delete]           ║ │
│  ║      [✓ Compliant]  [Confidence: 87.5%]                      ║ │
│  ║      📌 Extracted Information: [GST: 34] [Amount: 156]...    ║ │
│  ║      📅 Processed: Jan 15, 2025, 10:30 AM                    ║ │
│  ╚═══════════════════════════════════════════════════════════════╝ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ☐  📄 purchase_receipt_2024.pdf       [⬇️ Download]        │   │
│  │      Type: Purchase Receipt            [🗑️ Delete]          │   │
│  │      [⚠️ Partial Information]  [Confidence: 65.0%]          │   │
│  │      📌 Extracted Information: [GST: 12] [Amount: 45]...    │   │
│  │      📅 Processed: Jan 14, 2025, 3:15 PM                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌═══════════════════════════════════════════════════════════════┐ │ ← Selected
│  ║  ☑️  📄 bank_statement_dec.xlsx        [⬇️ Download]         ║ │
│  ║      Type: Bank Statement              [🗑️ Delete]          ║ │
│  ║      [ℹ️ Basic Information]  [Confidence: 72.3%]            ║ │
│  ║      📌 Extracted Information: [Date: 89] [Amount: 234]...  ║ │
│  ║      📅 Processed: Jan 13, 2025, 9:45 AM                    ║ │
│  ╚═══════════════════════════════════════════════════════════════╝ │
│                                                                       │
│  ┌═══════════════════════════════════════════════════════════════┐ │ ← Selected
│  ║  ☑️  📄 gst_return_q4.pdf              [⬇️ Download]         ║ │
│  ║      Type: Tax Return                  [🗑️ Delete]          ║ │
│  ║      [✓ Compliant]  [Confidence: 91.2%]                      ║ │
│  ║      📌 Extracted Information: [GST: 56] [Date: 34]...      ║ │
│  ║      📅 Processed: Jan 12, 2025, 2:20 PM                    ║ │
│  ╚═══════════════════════════════════════════════════════════════╝ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎬 User Interaction Flows

### **Flow 1: Download a Document**

```
1. User hovers over Download button
   ┌─────────────────┐
   │ ⬇️ Download     │ ← Hover effect (darker border)
   └─────────────────┘

2. User clicks Download button
   ┌─────────────────┐
   │ ⬇️ Download     │ ← Click animation
   └─────────────────┘

3. Toast notification appears
   ┌─────────────────────────────────────┐
   │ ✅ Download Successful              │
   │ tax_invoice_2024.xlsx report        │
   │ downloaded successfully.            │
   └─────────────────────────────────────┘

4. File downloads to browser's download folder
   📥 tax_invoice_2024_report.json
```

---

### **Flow 2: Delete a Single Document**

```
1. User clicks Delete button
   ┌─────────────────┐
   │ 🗑️ Delete       │ ← Red text, hover effect
   └─────────────────┘

2. Confirmation dialog appears
   ┌─────────────────────────────────────────────┐
   │  ⚠️ Confirm Deletion                        │
   │                                              │
   │  Are you sure you want to delete            │
   │  "tax_invoice_2024.xlsx"?                   │
   │                                              │
   │         [Cancel]  [Delete]                  │
   └─────────────────────────────────────────────┘

3. If confirmed, document card fades out
   ┌─────────────────────────────────────┐
   │  📄 tax_invoice_2024.xlsx           │ ← Fading...
   │  ...                                 │
   └─────────────────────────────────────┘

4. Toast notification appears
   ┌─────────────────────────────────────┐
   │ ✅ Document Deleted                 │
   │ tax_invoice_2024.xlsx has been      │
   │ deleted successfully.               │
   └─────────────────────────────────────┘

5. Document disappears from list
   (List automatically refreshes)
```

---

### **Flow 3: Multi-Select and Bulk Delete**

```
1. User clicks checkbox on first document
   ☐ → ☑️  (Card gets blue ring and background)

2. User clicks checkbox on second document
   ☐ → ☑️  (Card gets blue ring and background)

3. User clicks checkbox on third document
   ☐ → ☑️  (Card gets blue ring and background)

4. Toolbar updates in real-time
   ┌─────────────────────────────────────────────┐
   │ [☐ Select All]  [3 selected]                │
   │                  [🗑️ Delete 3 Document(s)]  │
   └─────────────────────────────────────────────┘

5. User clicks "Delete 3 Document(s)" button
   ┌─────────────────────────────────────────────┐
   │  ⚠️ Confirm Bulk Deletion                   │
   │                                              │
   │  Are you sure you want to delete            │
   │  3 document(s)?                             │
   │                                              │
   │         [Cancel]  [Delete]                  │
   └─────────────────────────────────────────────┘

6. If confirmed, all selected cards fade out
   ┌═══════════════════════════════════════┐
   ║  ☑️ Document 1...                     ║ ← Fading...
   ╚═══════════════════════════════════════╝
   ┌═══════════════════════════════════════┐
   ║  ☑️ Document 2...                     ║ ← Fading...
   ╚═══════════════════════════════════════╝
   ┌═══════════════════════════════════════┐
   ║  ☑️ Document 3...                     ║ ← Fading...
   ╚═══════════════════════════════════════╝

7. Toast notification appears
   ┌─────────────────────────────────────┐
   │ ✅ Documents Deleted                │
   │ 3 document(s) deleted successfully. │
   └─────────────────────────────────────┘

8. Selection cleared, list refreshes
   ┌─────────────────────────────────────────────┐
   │ [☐ Select All]                              │
   └─────────────────────────────────────────────┘
   (Remaining documents shown)
```

---

### **Flow 4: Select All / Deselect All**

```
1. Initial state - no selections
   ┌─────────────────────────────────────────────┐
   │ [☐ Select All]                              │
   └─────────────────────────────────────────────┘
   
   ☐ Document 1
   ☐ Document 2
   ☐ Document 3
   ☐ Document 4

2. User clicks "Select All"
   ┌─────────────────────────────────────────────┐
   │ [☑️ Deselect All]  [4 selected]             │
   │                     [🗑️ Delete 4 Document(s)]│
   └─────────────────────────────────────────────┘
   
   ☑️ Document 1  ← Blue ring
   ☑️ Document 2  ← Blue ring
   ☑️ Document 3  ← Blue ring
   ☑️ Document 4  ← Blue ring

3. User clicks "Deselect All"
   ┌─────────────────────────────────────────────┐
   │ [☐ Select All]                              │
   └─────────────────────────────────────────────┘
   
   ☐ Document 1
   ☐ Document 2
   ☐ Document 3
   ☐ Document 4
```

---

## 🎨 Color Coding

### **Classification Badges**

```
✅ Compliant
┌─────────────────┐
│ ✓ Compliant     │ ← Green background, green text, green border
└─────────────────┘

ℹ️ Basic Information
┌─────────────────────────┐
│ ℹ️ Basic Information    │ ← Blue background, blue text, blue border
└─────────────────────────┘

⚠️ Partial Information
┌─────────────────────────┐
│ ⚠️ Partial Information  │ ← Yellow background, yellow text, yellow border
└─────────────────────────┘

❌ Missing Key Information
┌─────────────────────────────┐
│ ❌ Missing Key Information  │ ← Red background, red text, red border
└─────────────────────────────┘
```

### **Button States**

```
Download Button (Normal)
┌─────────────────┐
│ ⬇️ Download     │ ← Gray border, white background
└─────────────────┘

Download Button (Hover)
┌─────────────────┐
│ ⬇️ Download     │ ← Darker border, light gray background
└─────────────────┘

Delete Button (Normal)
┌─────────────────┐
│ 🗑️ Delete       │ ← Gray border, red text
└─────────────────┘

Delete Button (Hover)
┌─────────────────┐
│ 🗑️ Delete       │ ← Red border, light red background, red text
└─────────────────┘

Delete Button (Disabled)
┌─────────────────┐
│ 🗑️ Deleting...  │ ← Gray, not clickable
└─────────────────┘

Bulk Delete Button
┌──────────────────────────┐
│ 🗑️ Delete 3 Document(s)  │ ← Red background, white text
└──────────────────────────┘
```

---

## 📱 Responsive Design

### **Desktop (Large Screens)**
- Entity cards: 4 columns
- Full button text: "Download", "Delete"
- Toolbar: Full width with space between elements

### **Tablet (Medium Screens)**
- Entity cards: 3 columns
- Full button text maintained
- Toolbar: Slightly compressed

### **Mobile (Small Screens)**
- Entity cards: 2 columns
- Buttons stack vertically
- Toolbar: Stacked layout
  - Select All button on top
  - Delete button below

---

## ✨ Animation & Transitions

### **Hover Effects**
- **Buttons**: Scale slightly, change border color
- **Cards**: Shadow increases on hover
- **Checkboxes**: Color change on hover

### **Selection Transitions**
- **Card Selection**: Smooth fade-in of blue ring and background (300ms)
- **Checkbox**: Instant toggle with smooth icon transition

### **Delete Animations**
- **Card Removal**: Fade out (200ms) then collapse
- **List Reflow**: Smooth repositioning of remaining cards

### **Toast Notifications**
- **Slide In**: From top-right corner
- **Auto Dismiss**: After 5 seconds
- **Slide Out**: Smooth exit animation

---

## 🔔 Toast Notification Examples

### **Success Notifications**

```
┌─────────────────────────────────────┐
│ ✅ Download Successful              │
│ tax_invoice_2024.xlsx report        │
│ downloaded successfully.            │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ✅ Document Deleted                 │
│ tax_invoice_2024.xlsx has been      │
│ deleted successfully.               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ✅ Documents Deleted                │
│ 3 document(s) deleted successfully. │
└─────────────────────────────────────┘
```

### **Error Notifications**

```
┌─────────────────────────────────────┐
│ ❌ Download Failed                  │
│ Failed to download document.        │
│ Please try again.                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ❌ Delete Failed                    │
│ Failed to delete document.          │
│ Please try again.                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ❌ No Documents Selected            │
│ Please select documents to delete.  │
└─────────────────────────────────────┘
```

---

## 🎯 Visual Hierarchy

### **Priority Levels**

1. **Primary Actions** (Most Important)
   - Bulk Delete button (red, prominent)
   - Document count badge (top right)

2. **Secondary Actions** (Important)
   - Individual Download/Delete buttons
   - Select All button

3. **Tertiary Elements** (Supporting)
   - Checkboxes
   - Selection counter badge
   - Entity summary cards

4. **Background Elements** (Context)
   - Classification badges
   - Timestamps
   - File type labels

---

## 📐 Spacing & Layout

### **Card Spacing**
- **Gap between cards**: 16px (1rem)
- **Padding inside cards**: 24px (1.5rem)
- **Margin around checkboxes**: 4px

### **Toolbar Spacing**
- **Height**: 64px
- **Padding**: 24px horizontal, 16px vertical
- **Gap between elements**: 16px

### **Button Spacing**
- **Gap between Download and Delete**: 8px
- **Padding inside buttons**: 8px horizontal, 4px vertical
- **Icon margin**: 8px right

---

## 🎨 Complete Color Palette

```
Primary Blue (Intelligence Blue):
- Ring: #3b82f6
- Background tint: rgba(59, 130, 246, 0.05)
- Text: #3b82f6

Success Green:
- Background: rgba(34, 197, 94, 0.1)
- Text: #16a34a
- Border: rgba(34, 197, 94, 0.2)

Warning Yellow:
- Background: rgba(234, 179, 8, 0.1)
- Text: #ca8a04
- Border: rgba(234, 179, 8, 0.2)

Error Red:
- Background: rgba(239, 68, 68, 0.1)
- Text: #dc2626
- Border: rgba(239, 68, 68, 0.2)
- Button: #ef4444

Neutral Gray:
- Muted background: rgba(0, 0, 0, 0.05)
- Border: rgba(0, 0, 0, 0.1)
- Text: #6b7280
```

---

## 🖼️ Icon Reference

| Icon | Component | Meaning |
|------|-----------|---------|
| ☐ | Square | Unselected checkbox |
| ☑️ | CheckSquare | Selected checkbox |
| 📄 | FileText | Document file |
| ⬇️ | Download | Download action |
| 🗑️ | Trash2 | Delete action |
| 🔍 | Search | Search functionality |
| ✓ | CheckCircle | Compliant status |
| ⚠️ | AlertCircle | Warning status |
| 📅 | Calendar | Date/timestamp |
| 📌 | Tag | Entity tags |

---

**This UI guide provides a complete visual reference for the document actions functionality!** 🎨✨
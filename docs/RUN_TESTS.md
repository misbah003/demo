# Quick Test Guide

## 🚀 Quick Start

### Step 1: Start the Backend Server
```bash
cd backend-example
node server.js
```

**Expected Output:**
```
🚀 Gmail OTP API server running on port 3001
📧 Gmail user: your-email@gmail.com
🔐 Gmail app password: Configured
```

### Step 2: Run the Test Script (in a new terminal)
```bash
python test_processing.py
```

**Expected Output:**
```
✅ Backend server is running

🔄 REGENERATING SAMPLE INVOICES
============================================================

✅ Generated: sample_invoice_1.pdf
   - Invoice: INV-1234
   - Seller: Acme Trading Pvt Ltd (GSTIN12345678)
   - Customer: BlueWave Imports (GSTIN87654321)
   - Date: 2024-12-20
   - Total: ₹1234.56

   📊 Processing Result:
      Type: Tax Invoice
      Classification: Compliant
      Confidence: 85.0%
      Entities: 12 found
      Sample entities:
         • GST: GSTIN12345678
         • GST: GSTIN87654321
         • Date: 2024-12-20
         • Invoice: INV-1234
         • Amount: ₹1234.56
         ... and 7 more
```

## 📊 What to Look For

### ✅ Good Results
- **Classification**: "Compliant" or "Basic Information Present"
- **Confidence**: 70-100%
- **Entities**: 8+ entities found
- **Types**: GST numbers, dates, amounts, invoice numbers

### ⚠️ Acceptable Results
- **Classification**: "Partial Information"
- **Confidence**: 50-70%
- **Entities**: 4-7 entities found

### ❌ Problem Indicators
- **Classification**: "Processing Failed" or "Missing Key Information"
- **Confidence**: 0-50%
- **Entities**: 0-3 entities found
- **Error messages** in output

## 🔍 Troubleshooting

### Backend Not Running
```
❌ Backend server is not running!
   Please start it with: node backend-example/server.js
```

**Solution:**
```bash
cd backend-example
node server.js
```

### Connection Refused
```
⚠️ Backend not running at http://localhost:3001
```

**Solution:**
1. Check if backend is running
2. Verify port 3001 is not in use
3. Check firewall settings

### Low Confidence Scores
```
Confidence: 30.0%
Entities: 2 found
```

**Solution:**
1. Check backend logs for extraction errors
2. Verify PDF generation is working
3. Check OCR dependencies are installed

### Processing Failed
```
Type: Error
Classification: Processing Failed
Confidence: 0.0%
```

**Solution:**
1. Check backend logs for specific errors
2. Verify tesseract.js is installed: `npm list tesseract.js`
3. Check pdf-parse is installed: `npm list pdf-parse`
4. Try regenerating the PDF

## 📝 Backend Logs to Monitor

### Good Extraction
```
=== Processing sample_invoice_1.pdf ===
✅ Direct text extraction successful (1234 chars)
Extracted text length: 1234
Entities found: 12 entities
  - GST: GSTIN12345678
  - GST: GSTIN87654321
  - Date: 2024-12-20
  - Invoice: INV-1234
  - Amount: ₹1234.56
  ... and 7 more
Type: Tax Invoice
Classification: Compliant
Confidence: 85.0%
✅ Document saved to database
```

### OCR Fallback (Still OK)
```
=== Processing sample_invoice_2.pdf ===
⚠️ Direct text extraction yielded minimal text, trying OCR...
✅ OCR successful
Entities found: 10 entities
Type: Tax Invoice
Classification: Compliant
Confidence: 75.0%
```

### Failed Extraction
```
=== Processing sample_invoice_5.pdf ===
❌ PDF extraction error: ...
🔄 Trying OCR fallback...
❌ OCR fallback also failed: ...
⚠️ Returning empty text - document will be marked as failed
⚠️ Insufficient text extracted from document
```

## 🎯 Success Criteria

After running the test, you should see:

- ✅ **4-5 out of 5** documents marked as "Compliant" or "Basic Information Present"
- ✅ **Average confidence** above 70%
- ✅ **8-15 entities** extracted per document
- ✅ **All key fields** present: GST, Date, Invoice, Amount, Company
- ✅ **No server crashes** or unhandled errors

## 🔄 Re-running Tests

To test again with fresh data:

```bash
# The test script automatically generates new PDFs each time
python test_processing.py
```

Each run creates new random invoices with different:
- Invoice numbers
- Company names
- Dates
- Amounts
- GST numbers

## 📦 Dependencies Check

If you encounter issues, verify all dependencies are installed:

```bash
cd backend-example
npm list tesseract.js pdf-parse pdf2pic multer @supabase/supabase-js
```

**Expected:**
```
backend-example@1.0.0
├── tesseract.js@5.x.x
├── pdf-parse@1.x.x
├── pdf2pic@2.x.x
├── multer@1.x.x
└── @supabase/supabase-js@2.x.x
```

If any are missing:
```bash
npm install
```

## 🐛 Debug Mode

For detailed debugging, use the debug endpoint:

```bash
curl -X POST http://localhost:3001/api/debug-extract \
  -F "document=@sample_documents/sample_invoice_1.pdf"
```

This returns:
- Full extracted text
- All entities found
- Document type
- Classification
- No database save (for testing only)

## 📞 Need Help?

1. Check `DOCUMENT_PROCESSING_FIX.md` for detailed fix information
2. Review backend logs for specific errors
3. Verify all dependencies are installed
4. Check that PDFs are being generated correctly
5. Ensure Supabase connection is working (if using database)

## ✨ What's Fixed

This test validates the following fixes:

1. ✅ **Better Amount Extraction** - Captures more amount formats
2. ✅ **Improved Compliance Logic** - More lenient classification
3. ✅ **Enhanced Error Handling** - Graceful failure recovery
4. ✅ **Confidence Calculation** - Based on actual data quality
5. ✅ **Better Logging** - Easier debugging and monitoring
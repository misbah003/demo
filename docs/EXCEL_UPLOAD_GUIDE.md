# 📊 Excel Document Upload Guide

## ✅ **Excel Support is Now Enabled!**

The Tax Intelligence Platform now supports **Excel files (.xlsx, .xls)** in addition to PDF and image files.

---

## 🎯 **How to Upload Excel Documents**

### **Option 1: Use the Web Interface**

1. **Open the site:** http://localhost:8080
2. **Login** to your account
3. **Navigate to** the document upload section
4. **Click "Upload"** or drag-and-drop your Excel files
5. **Supported formats:** `.xlsx`, `.xls`

### **Option 2: Generate Sample Excel Files**

Run the sample document generator:

```bash
python sample_doc.py
```

This will:
- ✅ Generate 5 individual invoice Excel files
- ✅ Automatically upload them to the backend
- ✅ Create a comprehensive Excel file with all document types
- ✅ Save files in `sample_documents/` folder

---

## 📋 **What Excel Files Can Contain**

The system can extract and process:

- **Tax Invoices** - Invoice numbers, dates, amounts, GST numbers
- **Tax Returns** - Filing dates, turnover, VAT paid, refund claims
- **Financial Statements** - Revenue, expenses, profit/loss, assets, liabilities
- **Bank Statements** - Transactions, dates, amounts, balances
- **Receipts** - Receipt IDs, payer/payee info, amounts, VAT

---

## 🔍 **What the System Extracts**

From your Excel files, the system automatically identifies:

- ✅ **GST Numbers** (e.g., GSTIN12345678)
- ✅ **PAN Numbers**
- ✅ **Invoice Numbers** (e.g., INV-1234)
- ✅ **Amounts** (₹, INR, Rs.)
- ✅ **Dates** (various formats)
- ✅ **Company Names**

---

## 📊 **Sample Files Generated**

### **Individual Invoice Files:**
- `sample_invoice_1.xlsx`
- `sample_invoice_2.xlsx`
- `sample_invoice_3.xlsx`
- `sample_invoice_4.xlsx`
- `sample_invoice_5.xlsx`

### **Comprehensive File:**
- `tax_documents_sample.xlsx` - Contains 5 sheets:
  - **Invoices** - Multiple invoice records
  - **Tax Returns** - Tax filing information
  - **Financial Statements** - Company financials
  - **Bank Statements** - Transaction history
  - **Receipts** - Payment receipts

---

## ✅ **Compliance Checking**

The system checks for:

- **Compliant:** Has GST + Date + Invoice Number + Amount
- **Basic Information Present:** Has some key fields
- **Partial Information:** Has at least one identifier
- **Missing Key Information:** Incomplete data

---

## 🛠️ **Technical Details**

### **Backend Changes:**
- ✅ Added `xlsx` npm package for Excel parsing
- ✅ Updated file filter to accept `.xlsx` and `.xls` files
- ✅ Added `extractTextFromExcel()` function
- ✅ Processes all sheets in Excel workbooks
- ✅ Converts data to text for entity extraction

### **Supported MIME Types:**
- `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (.xlsx)
- `application/vnd.ms-excel` (.xls)

### **File Size Limit:**
- Maximum: **10MB** per file

---

## 🎉 **Quick Test**

To quickly test Excel upload:

1. **Run the generator:**
   ```bash
   python sample_doc.py
   ```

2. **Check the output:**
   - You should see: `✅ sample_invoice_X.xlsx uploaded and processed successfully.`

3. **View in the web interface:**
   - Open http://localhost:8080
   - Login and check your documents dashboard
   - You should see the processed Excel files with extracted data

---

## 📝 **Example Excel Structure**

### **Invoice Sheet:**
```
| Invoice No | Date       | Seller          | GSTIN        | Amount  |
|------------|------------|-----------------|--------------|---------|
| INV-1234   | 2025-01-15 | Acme Trading    | GSTIN1234567 | 5000.00 |
```

The system will extract:
- Invoice: INV-1234
- Date: 2025-01-15
- Company: Acme Trading
- GST: GSTIN1234567
- Amount: 5000.00

---

## 🔧 **Troubleshooting**

### **Upload fails with "Only PDF and image files allowed"**
- ✅ **Fixed!** Backend now accepts Excel files
- Make sure backend server is restarted after the update

### **No data extracted from Excel**
- Check if the Excel file has data in the first sheet
- Ensure cells contain text/numbers (not formulas only)
- Try the sample generator to create a known-good file

### **Backend returns 500 error**
- Check backend console for error messages
- Ensure `xlsx` package is installed: `npm install xlsx`
- Restart the backend server

---

## 📞 **Need Help?**

If you encounter issues:
1. Check `TROUBLESHOOTING.md` for common problems
2. View backend logs in the blue PowerShell window
3. Ensure both servers are running (backend + frontend)

---

**Happy document processing! 📊✨**
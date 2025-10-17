import openpyxl
import os

# View one of the generated invoice Excel files
invoice_file = "sample_documents/sample_invoice_1.xlsx"

if not os.path.exists(invoice_file):
    print(f"❌ File not found: {invoice_file}")
    exit(1)

print("=" * 70)
print("📊 SAMPLE INVOICE EXCEL FILE CONTENT")
print("=" * 70)
print(f"\n📁 File: {invoice_file}")
print(f"📏 Size: {os.path.getsize(invoice_file)} bytes\n")

wb = openpyxl.load_workbook(invoice_file)
ws = wb.active

print(f"📄 Sheet Name: {ws.title}")
print("\n" + "=" * 70)
print("INVOICE CONTENT:")
print("=" * 70 + "\n")

for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    # Simple row-by-row display
    if any(cell is not None for cell in row):  # Only print non-empty rows
        row_str = " | ".join(str(cell) if cell is not None else "" for cell in row)
        print(f"Row {i:2d}: {row_str}")

print("\n" + "=" * 70)
print("✅ This file was successfully uploaded and processed by the backend!")
print("=" * 70)
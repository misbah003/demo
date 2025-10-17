import os
from openpyxl import Workbook

# Test creating a simple Excel file
sample_dir = "sample_documents"
if not os.path.exists(sample_dir):
    os.makedirs(sample_dir)
    print(f"📁 Created {sample_dir}/ folder")

# Create a test Excel file
wb = Workbook()
ws = wb.active
ws.title = "Test"
ws.append(["Test", "Data"])
ws.append(["Hello", "World"])

test_file = os.path.join(sample_dir, "test_excel.xlsx")
wb.save(test_file)
print(f"✅ Created test file: {test_file}")

# Check if it exists
if os.path.exists(test_file):
    print(f"✅ File exists! Size: {os.path.getsize(test_file)} bytes")
else:
    print(f"❌ File does not exist!")

# List all files in sample_documents
print(f"\n📁 Files in {sample_dir}:")
for file in os.listdir(sample_dir):
    filepath = os.path.join(sample_dir, file)
    print(f"  - {file} ({os.path.getsize(filepath)} bytes)")
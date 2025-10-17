"""
Test script to regenerate sample PDFs and upload them to the backend
"""
import os
import sys
import requests
import time

# Add the current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from sample_doc import generate_invoice, create_invoice_pdf

def test_document_processing():
    """Generate and test document processing"""
    
    # Create sample_documents folder if it doesn't exist
    sample_dir = "sample_documents"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
        print(f"📁 Created {sample_dir}/ folder")
    
    print("\n" + "="*60)
    print("🔄 REGENERATING SAMPLE INVOICES")
    print("="*60 + "\n")
    
    # Generate and upload 5 invoices
    for i in range(5):
        inv = generate_invoice()
        filename = f"sample_invoice_{i+1}.pdf"
        filepath = os.path.join(sample_dir, filename)
        
        # Create PDF
        create_invoice_pdf(inv, filepath)
        print(f"✅ Generated: {filename}")
        print(f"   - Invoice: {inv['invoice_number']}")
        print(f"   - Seller: {inv['seller']['company_name']} ({inv['seller']['tax_id']})")
        print(f"   - Customer: {inv['customer']['company_name']} ({inv['customer']['tax_id']})")
        print(f"   - Date: {inv['invoice_date']}")
        print(f"   - Total: ₹{inv['total']:.2f}")
        
        # Upload to backend
        try:
            with open(filepath, 'rb') as f:
                files = {'documents': (filename, f, 'application/pdf')}
                response = requests.post('http://localhost:3001/api/process-document', files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success') and result.get('results'):
                        doc_result = result['results'][0]
                        print(f"\n   📊 Processing Result:")
                        print(f"      Type: {doc_result.get('type', 'N/A')}")
                        print(f"      Classification: {doc_result.get('classification', 'N/A')}")
                        print(f"      Confidence: {doc_result.get('confidence', 0)*100:.1f}%")
                        print(f"      Entities: {len(doc_result.get('entities', []))} found")
                        
                        # Show some entities
                        entities = doc_result.get('entities', [])
                        if entities:
                            print(f"      Sample entities:")
                            for entity in entities[:5]:
                                print(f"         • {entity}")
                            if len(entities) > 5:
                                print(f"         ... and {len(entities) - 5} more")
                    else:
                        print(f"   ❌ Processing failed: {result}")
                else:
                    print(f"   ❌ Upload failed: HTTP {response.status_code}")
                    print(f"      Response: {response.text[:200]}")
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️ Backend not running at http://localhost:3001")
            print(f"      Please start the backend server first!")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        time.sleep(0.5)  # Small delay between uploads
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETE")
    print("="*60)
    return True

if __name__ == "__main__":
    print("\n🚀 Starting Document Processing Test\n")
    
    # Check if backend is running
    try:
        response = requests.get('http://localhost:3001/api/health', timeout=2)
        if response.status_code == 200:
            print("✅ Backend server is running\n")
        else:
            print("⚠️ Backend server responded with unexpected status\n")
    except:
        print("❌ Backend server is not running!")
        print("   Please start it with: node backend-example/server.js")
        print("   Or use: npm start (if configured)\n")
        sys.exit(1)
    
    # Run the test
    success = test_document_processing()
    
    if success:
        print("\n✅ All documents generated and uploaded successfully!")
    else:
        print("\n⚠️ Some issues occurred during processing")
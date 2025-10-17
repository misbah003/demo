// Test script to verify Excel entity extraction
const XLSX = require('xlsx');

function extractEntities(text) {
  const entities = [];

  // GST Number patterns (Indian GST) - ENHANCED for Excel data
  const gstPatterns = [
    /\bGSTIN\s*:?\s*\d{8,15}\b/gi, // GSTIN followed by 8-15 digits (flexible)
    /\bGSTIN\d{8,15}\b/gi, // GSTIN directly followed by digits
    /\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}[A-Z]{1}\d{1}\b/g, // Standard GST format
    /\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[A-Z]{1}\d{1}\b/g, // Variations
    /GST\s*(?:Number|No|#)?\s*:?\s*[\dA-Z]{10,15}/gi // GST with various labels
  ];

  gstPatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        entities.push(`GST: ${match.trim()}`);
      });
    }
  });

  // Amount patterns - ENHANCED for Excel and various formats
  const amountPatterns = [
    /₹\s*[\d,]+(?:\.\d{1,2})?/g, // ₹ with optional space
    /INR\s*[\d,]+(?:\.\d{1,2})?/gi,
    /Rs\.?\s*[\d,]+(?:\.\d{1,2})?/gi,
    /(?:Total|Subtotal|Amount|VAT|Tax|Rate|Refund|Price|Value)[\s:]+₹?\s*[\d,]+(?:\.\d{1,2})?/gi, // With labels
    /\b[\d,]{1,}[\d]+\.\d{2}\b/g, // Decimal numbers with commas (e.g., 94,612.20)
    /\b[\d]{1,3}(?:,\d{3})*(?:\.\d{2})?\b/g, // Numbers with thousand separators
    /\b[\d]+\.[\d]{2}\b/g // Numbers with exactly 2 decimal places
  ];

  const foundAmounts = new Set();
  amountPatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        const cleanMatch = match.trim();
        const numPart = cleanMatch.replace(/[^\d.,]/g, '');
        const numValue = parseFloat(numPart.replace(/,/g, ''));
        if (!foundAmounts.has(numPart) && numValue > 10) {
          foundAmounts.add(numPart);
          entities.push(`MONEY: ${numPart}`);
        }
      });
    }
  });

  // Date patterns
  const datePatterns = [
    /\b\d{1,2}[-\/]\d{1,2}[-\/]\d{4}\b/g,
    /\b\d{4}[-\/]\d{1,2}[-\/]\d{1,2}\b/g,
    /\b\d{4}-\d{2}-\d{2}\b/g,
    /\b\d{1,2}\/\d{1,2}\/\d{4}\b/g
  ];

  datePatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        entities.push(`Date: ${match}`);
      });
    }
  });

  // Invoice numbers - ENHANCED patterns
  const invoicePatterns = [
    /\bINV-\d{4,}\b/gi,
    /\bInvoice\s*(?:Number|No|#)?\s*:?\s*[\dA-Z-]+/gi,
    /\b[A-Z]{2,4}-\d{4,}\b/g
  ];

  invoicePatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        entities.push(`Invoice: ${match.trim()}`);
      });
    }
  });

  return [...new Set(entities)];
}

function checkCompliance(entities) {
  const hasGST = entities.some(entity => entity.includes('GST:'));
  const hasAmount = entities.some(entity => entity.includes('Amount:') || entity.includes('MONEY:'));
  const hasDate = entities.some(entity => entity.includes('Date:'));
  const hasInvoice = entities.some(entity => entity.includes('Invoice:'));

  const keyFieldsCount = [hasGST, hasDate, hasInvoice, hasAmount].filter(Boolean).length;

  if (hasGST && hasDate && hasInvoice) {
    return 'Compliant';
  } else if (hasGST && hasAmount && (hasDate || hasInvoice)) {
    return 'Compliant';
  } else if (hasGST && keyFieldsCount >= 2) {
    return 'Compliant';
  } else if (hasAmount && hasDate) {
    return 'Basic Information Present';
  } else if (hasGST || hasInvoice) {
    return 'Partial Information';
  } else if (hasAmount) {
    return 'Partial Information';
  } else {
    return 'Missing Key Information';
  }
}

// Test files
const testFiles = [
  'C:\\Users\\HomeLaptop\\Downloads\\vat-refund-report-2025-10-11.xlsx',
  'C:\\Users\\HomeLaptop\\Downloads\\navi-tax-35-main\\data\\sample_documents\\sample_invoice_3.xlsx'
];

console.log('🧪 Testing Excel Entity Extraction\n');
console.log('='.repeat(80));

testFiles.forEach((filePath, index) => {
  console.log(`\n📄 Test ${index + 1}: ${filePath.split('\\').pop()}`);
  console.log('-'.repeat(80));
  
  try {
    const workbook = XLSX.readFile(filePath);
    let allText = '';
    
    workbook.SheetNames.forEach(sheetName => {
      const worksheet = workbook.Sheets[sheetName];
      const csvText = XLSX.utils.sheet_to_csv(worksheet);
      allText += `\n${csvText}\n`;
    });
    
    console.log(`\n📝 Extracted Text (first 500 chars):`);
    console.log(allText.substring(0, 500));
    console.log('...\n');
    
    const entities = extractEntities(allText);
    const compliance = checkCompliance(entities);
    
    console.log(`\n✅ Entities Found (${entities.length}):`);
    entities.forEach(entity => console.log(`   - ${entity}`));
    
    console.log(`\n📊 Compliance Status: ${compliance}`);
    
    // Check for VAT forecast compatibility
    const moneyEntities = entities.filter(e => e.includes('MONEY:'));
    console.log(`\n💰 Money Values for VAT Forecast: ${moneyEntities.length}`);
    if (moneyEntities.length > 0) {
      console.log('   ✅ This document CAN be used for VAT forecasting');
    } else {
      console.log('   ❌ This document CANNOT be used for VAT forecasting (no money values)');
    }
    
  } catch (error) {
    console.error(`❌ Error processing file: ${error.message}`);
  }
  
  console.log('\n' + '='.repeat(80));
});

console.log('\n✅ Test Complete!\n');
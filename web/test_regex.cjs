const fs = require('fs');

function extractEntities(text) {
  const entities = [];

  // GST Number patterns (Indian GST) - updated to match GSTIN prefix
  const gstPatterns = [
    /\bGSTIN\d{8}\b/g, // GSTIN followed by 8 digits
    /\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}[A-Z]{1}\d{1}\b/g, // Standard GST format
    /\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[A-Z]{1}\d{1}\b/g // Variations
  ];

  gstPatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        entities.push(`GST: ${match}`);
      });
    }
  });

  // Amount patterns (₹ symbol or INR) - more flexible
  const amountPatterns = [
    /₹\s*[\d,]+(?:\.\d{2})?/g, // ₹ with optional space
    /INR\s*[\d,]+(?:\.\d{2})?/gi,
    /Rs\.?\s*[\d,]+(?:\.\d{2})?/gi
  ];

  amountPatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        entities.push(`Amount: ${match.trim()}`);
      });
    }
  });

  // Date patterns - updated to match ISO format
  const datePatterns = [
    /\b\d{1,2}[-\/]\d{1,2}[-\/]\d{4}\b/g, // DD/MM/YYYY or DD-MM-YYYY
    /\b\d{4}[-\/]\d{1,2}[-\/]\d{1,2}\b/g, // YYYY/MM/DD or YYYY-MM-DD
    /\b\d{4}-\d{2}-\d{2}\b/g // ISO format specifically
  ];

  datePatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) {
      matches.forEach(match => {
        entities.push(`Date: ${match}`);
      });
    }
  });

  // Company names (simple heuristic: capitalized words)
  const companyPattern = /\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Ltd|Pvt|Private|Limited|Corp|Corporation|Inc|LLC))?\b/g;
  const companyMatches = text.match(companyPattern);
  if (companyMatches) {
    companyMatches.forEach(match => {
      entities.push(`Company: ${match}`);
    });
  }

  // Invoice numbers
  const invoicePattern = /\bINV-\d{4}\b/g;
  const invoiceMatches = text.match(invoicePattern);
  if (invoiceMatches) {
    invoiceMatches.forEach(match => {
      entities.push(`Invoice: ${match}`);
    });
  }

  return [...new Set(entities)]; // Remove duplicates
}

// Test with our sample text
const text = fs.readFileSync('test_content.txt', 'utf8');
console.log('Input text:');
console.log(text);
console.log('\nExtracted entities:');
console.log(extractEntities(text));
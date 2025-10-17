const fs = require('fs');
const FormData = require('form-data');
const fetch = require('node-fetch');

async function testDebug() {
  const form = new FormData();
  const fileStream = fs.createReadStream('sample_invoice_3.pdf');
  form.append('document', fileStream, 'sample_invoice_3.pdf');

  try {
    const response = await fetch('http://localhost:3001/api/debug-extract', {
      method: 'POST',
      body: form
    });

    const result = await response.json();
    console.log('Debug Result:');
    console.log('============');
    console.log('Extracted Text:');
    console.log(result.extractedText);
    console.log('\nEntities:');
    console.log(result.entities);
    console.log('\nType:', result.type);
    console.log('Classification:', result.classification);
  } catch (error) {
    console.error('Error:', error);
  }
}

testDebug();
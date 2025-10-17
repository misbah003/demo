// Script to apply the migration to Supabase
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const supabase = createClient(
  'https://ikqcakganqabiscsibym.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrcWNha2dhbnFhYmlzY3NpYnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjc0NDIsImV4cCI6MjA3Mzk0MzQ0Mn0.hkfGO88f95rQO_7bwsRcxADjZRAjw5LoWFxmq5mNY90'
);

async function applyMigration() {
  console.log('📝 Reading migration file...');
  
  const migrationPath = path.join(__dirname, 'supabase', 'migrations', '20250101000001_add_processed_documents.sql');
  const sql = fs.readFileSync(migrationPath, 'utf8');
  
  console.log('🚀 Applying migration to Supabase...');
  console.log('\nNote: The anon key cannot execute DDL statements.');
  console.log('Please run this SQL manually in the Supabase SQL Editor:\n');
  console.log('=' .repeat(80));
  console.log(sql);
  console.log('=' .repeat(80));
  console.log('\nSteps:');
  console.log('1. Go to https://supabase.com/dashboard/project/ikqcakganqabiscsibym/sql/new');
  console.log('2. Copy the SQL above');
  console.log('3. Paste it into the SQL Editor');
  console.log('4. Click "Run" to execute');
}

applyMigration();
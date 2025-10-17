# ========================================
# Navi Tax Project - Cleanup & Organization
# ========================================
# This script organizes the project by moving
# unnecessary files to an archive folder
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PROJECT CLEANUP & ORGANIZATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = "C:\Users\HomeLaptop\Downloads\navi-tax-35-main"
Set-Location $ProjectRoot

# Create archive directory
Write-Host "[STEP 1/5] Creating archive directory..." -ForegroundColor Yellow
$ArchiveDir = "$ProjectRoot\archive"
if (-not (Test-Path $ArchiveDir)) {
    New-Item -ItemType Directory -Path $ArchiveDir -Force | Out-Null
    Write-Host "[OK] Archive directory created" -ForegroundColor Green
} else {
    Write-Host "[OK] Archive directory exists" -ForegroundColor Green
}
Write-Host ""

# Create subdirectories in archive
$ArchiveSubDirs = @(
    "$ArchiveDir\old-docs",
    "$ArchiveDir\old-scripts",
    "$ArchiveDir\old-models",
    "$ArchiveDir\test-files",
    "$ArchiveDir\temp-files"
)

foreach ($dir in $ArchiveSubDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# ========================================
# STEP 2: Move Old Documentation Files
# ========================================
Write-Host "[STEP 2/5] Moving old documentation files..." -ForegroundColor Yellow

$OldDocs = @(
    "ADDITIONAL_FIXES.md",
    "ADVANCED_ML_DOCUMENTATION.md",
    "API_READY.txt",
    "BEFORE_AFTER_COMPARISON.txt",
    "BEFORE_AFTER_YOUR_WEBSITE.txt",
    "COMPARISON_CHART.txt",
    "COMPLETE_FIX_SUMMARY.md",
    "DASHBOARD.txt",
    "DASHBOARD_25000_SAMPLES.txt",
    "DATE_PICKER_PROOF.md",
    "DEPLOYMENT_GUIDE.md",
    "ERROR_DIAGNOSIS.md",
    "EXCEL_PROCESSING_FIX.md",
    "EXECUTION_LOG.txt",
    "FAST_TRAINING_SOLUTION.txt",
    "FINAL_CHECKLIST.md",
    "FINAL_OPTIMIZED_SUMMARY.md",
    "FINAL_PROOF_SUMMARY.md",
    "FINAL_RESULTS_25000_SAMPLES.md",
    "FINAL_SUMMARY.md",
    "FINAL_SUMMARY.txt",
    "FIXES_COMPLETED.md",
    "FIX_BACKEND_AND_FORECAST.md",
    "HOW_TO_CHECK_PROGRESS.txt",
    "HOW_TO_VERIFY.md",
    "INDEX.md",
    "INTEGRATION_CODE_CHANGES.md",
    "INTEGRATION_DIAGRAM.md",
    "INTEGRATION_STEPS.html",
    "INTEGRATION_SUMMARY.md",
    "INTEGRATION_SUMMARY.txt",
    "MODEL_PERFORMANCE_EXPLAINED.md",
    "OPTIMIZED_MODEL_INTEGRATION_GUIDE.md",
    "OPTIMIZED_MODEL_README.md",
    "PROFILE_FIX_COMPLETE.md",
    "QUICK_ANSWER_REAL_DATA.txt",
    "QUICK_EXCEL_FIX_GUIDE.md",
    "QUICK_FIX_GUIDE.md",
    "QUICK_FIX_SUMMARY.md",
    "QUICK_START_GUIDE.md",
    "QUICK_START_YOUR_WEBSITE.txt",
    "README_FINAL_25000.md",
    "README_FIRST.txt",
    "README_OPTIMIZED_MODEL.md",
    "README_REAL_DATA.md",
    "README_TRAINING.txt",
    "READ_ME_FIRST.txt",
    "REAL_DATA_ANALYSIS.md",
    "RESULTS_SUMMARY.md",
    "SERVER_MANAGEMENT_GUIDE.md",
    "START_DEPLOYMENT.txt",
    "START_HERE.md",
    "START_HERE.txt",
    "START_HERE_25000_SAMPLES.txt",
    "START_HERE_OPTIMIZED.txt",
    "START_HERE_REAL_DATA.txt",
    "START_HERE_WEBSITE_INTEGRATION.txt",
    "STATE_INTEGRATION_SUMMARY.txt",
    "STEP_BY_STEP_REAL_DATA.md",
    "TEST_FIXES.md",
    "TRAINING_IN_PROGRESS.txt",
    "TRAINING_STATUS.md",
    "TROUBLESHOOTING_GUIDE.md",
    "VAT_FORECAST_FIX_COMPLETE.md",
    "VERIFY_REAL_CONNECTION.md",
    "VISUAL_COMPARISON_REAL_DATA.txt",
    "VISUAL_OPTIMIZED_SUMMARY.txt",
    "VISUAL_SUMMARY.txt",
    "WEBSITE_INTEGRATION_COMPLETE.md",
    "WEBSITE_INTEGRATION_GUIDE.md",
    "WEBSITE_INTEGRATION_WITH_STATES.md",
    "WHATS_NEW_WITH_STATES.md",
    "WHAT_CHANGED_SUMMARY.txt",
    "WHICH_FILE_TO_USE.txt",
    "YOUR_QUESTIONS_ANSWERED.md",
    "QUICK_FIX_STEPS.txt",
    "COMPLETE_SOLUTION.md",
    "INTEGRATION_COMPLETE.md",
    "ML_INSTALLATION_COMPLETE.md",
    "REAL_ML_SYSTEM_COMPLETE.md",
    "VAT_FORECAST_FIX_COMPLETE.txt",
    "WARNINGS_FIXED.md",
    "INSTALLATION_COMPLETE_NO_WARNINGS.txt",
    "DO_THIS_NOW.txt",
    "START_HERE_ML_SYSTEM.txt",
    "FILES_CREATED_SUMMARY.txt",
    "BEFORE_AFTER_COMPARISON.md",
    "ML_BEFORE_AFTER_COMPARISON.md",
    "ML_INTEGRATION_DIAGRAM.txt",
    "SCRIPTS_OVERVIEW.txt",
    "ALL_FILES_INDEX.md",
    "FIX_VAT_FORECAST.md",
    "ML_INTEGRATION_GUIDE.md",
    "START_HERE.md",
    "START_HERE_ADVANCED_ML.md"
)

$movedDocs = 0
foreach ($file in $OldDocs) {
    $sourcePath = "$ProjectRoot\$file"
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination "$ArchiveDir\old-docs\" -Force -ErrorAction SilentlyContinue
        $movedDocs++
    }
}
Write-Host "[OK] Moved $movedDocs old documentation files" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 3: Move Old/Duplicate Scripts
# ========================================
Write-Host "[STEP 3/5] Moving old/duplicate scripts..." -ForegroundColor Yellow

$OldScripts = @(
    "APPLY_ML_INTEGRATION.bat",
    "CHECK_BACKEND_STATUS.ps1",
    "CHECK_SERVERS.bat",
    "CHECK_TRAINING_STATUS.bat",
    "CHECK_WHAT_IS_RUNNING.bat",
    "INTEGRATE_ML_NOW.bat",
    "MONITOR_TRAINING.bat",
    "QUICK_START.bat",
    "quick_verify.ps1",
    "SETUP_ADVANCED_ML.bat",
    "simple_proof.ps1",
    "START_BACKEND.bat",
    "START_BOTH_SERVERS.bat",
    "START_FRONTEND.bat",
    "START_PROJECT.bat",
    "START_SERVERS.ps1",
    "STOP_SERVERS.bat",
    "TEST_ADVANCED_ML.bat",
    "test_api.ps1",
    "TRAIN_FAST.bat"
)

$movedScripts = 0
foreach ($file in $OldScripts) {
    $sourcePath = "$ProjectRoot\$file"
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination "$ArchiveDir\old-scripts\" -Force -ErrorAction SilentlyContinue
        $movedScripts++
    }
}
Write-Host "[OK] Moved $movedScripts old script files" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 4: Move Test Files
# ========================================
Write-Host "[STEP 4/5] Moving test files..." -ForegroundColor Yellow

$TestFiles = @(
    "test_date_picker.ps1",
    "test_date_picker_visual.html",
    "test_excel_extraction.js",
    "test_forecast_integration.html",
    "TEST_INVOICE.txt",
    "test_vat_predictor.html",
    "vat_predictor.js",
    "vat_refund_widget.html",
    "ai_tax (Autosaved).docx"
)

$movedTests = 0
foreach ($file in $TestFiles) {
    $sourcePath = "$ProjectRoot\$file"
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination "$ArchiveDir\test-files\" -Force -ErrorAction SilentlyContinue
        $movedTests++
    }
}
Write-Host "[OK] Moved $movedTests test files" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 5: Move Old Model Directories
# ========================================
Write-Host "[STEP 5/5] Moving old model directories..." -ForegroundColor Yellow

$OldModelDirs = @(
    "enhanced_models_1000_samples",
    "enhanced_models_25000_samples",
    "enhanced_synthetic_data"
)

$movedModels = 0
foreach ($dir in $OldModelDirs) {
    $sourcePath = "$ProjectRoot\$dir"
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination "$ArchiveDir\old-models\" -Force -ErrorAction SilentlyContinue
        $movedModels++
    }
}
Write-Host "[OK] Moved $movedModels old model directories" -ForegroundColor Green
Write-Host ""

# ========================================
# STEP 6: Clean up SQL files
# ========================================
Write-Host "[STEP 6/6] Moving SQL files..." -ForegroundColor Yellow

$SQLFiles = @(
    "APPLY_FIXES_MANUALLY.sql",
    "CHECK_DOCUMENTS.sql",
    "DELETE_OLD_DOCUMENTS.sql"
)

$movedSQL = 0
foreach ($file in $SQLFiles) {
    $sourcePath = "$ProjectRoot\$file"
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination "$ArchiveDir\old-docs\" -Force -ErrorAction SilentlyContinue
        $movedSQL++
    }
}
Write-Host "[OK] Moved $movedSQL SQL files" -ForegroundColor Green
Write-Host ""

# ========================================
# SUCCESS SUMMARY
# ========================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Files Organized:" -ForegroundColor Cyan
Write-Host "  - Documentation files: $movedDocs" -ForegroundColor White
Write-Host "  - Script files: $movedScripts" -ForegroundColor White
Write-Host "  - Test files: $movedTests" -ForegroundColor White
Write-Host "  - Model directories: $movedModels" -ForegroundColor White
Write-Host "  - SQL files: $movedSQL" -ForegroundColor White
Write-Host ""
Write-Host "All files moved to: $ArchiveDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  REMAINING STRUCTURE:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Essential Files Kept:" -ForegroundColor Green
Write-Host "  ✅ README.md                    - Main documentation" -ForegroundColor White
Write-Host "  ✅ START_ALL_SERVERS.ps1        - Start all services" -ForegroundColor White
Write-Host "  ✅ START_ADVANCED_ML_API.bat    - Start ML API only" -ForegroundColor White
Write-Host "  ✅ STOP_SERVERS.ps1             - Stop all services" -ForegroundColor White
Write-Host "  ✅ docker-compose.yml           - Docker deployment" -ForegroundColor White
Write-Host "  ✅ deploy.sh / deploy.bat       - Deployment scripts" -ForegroundColor White
Write-Host ""
Write-Host "Essential Directories:" -ForegroundColor Green
Write-Host "  ✅ docs/backend-example/        - Backend server" -ForegroundColor White
Write-Host "  ✅ web/                         - Frontend application" -ForegroundColor White
Write-Host "  ✅ ml/                          - ML API" -ForegroundColor White
Write-Host "  ✅ scripts/                     - Utility scripts" -ForegroundColor White
Write-Host "  ✅ models/                      - Trained ML models" -ForegroundColor White
Write-Host "  ✅ data/                        - Data files" -ForegroundColor White
Write-Host "  ✅ archive/                     - Archived old files" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your project is now clean and organized!" -ForegroundColor Green
Write-Host ""
Write-Host "To restore any archived files, check: $ArchiveDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
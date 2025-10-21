#!/usr/bin/env python3
"""
🚀 DEPLOYMENT READINESS CHECK
==============================

Validates all files and dependencies are ready for Render + Vercel deployment.
Run this BEFORE deploying to catch any issues early.

Usage:
    python DEPLOYMENT_READY_CHECK.py
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(path, name):
    """Check if file exists"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  ✅ {name} ({size:,} bytes)")
        return True
    else:
        print(f"  ❌ MISSING: {name}")
        return False

def check_directory_exists(path, name):
    """Check if directory exists"""
    if os.path.isdir(path):
        files = len(os.listdir(path))
        print(f"  ✅ {name} ({files} files)")
        return True
    else:
        print(f"  ❌ MISSING DIRECTORY: {name}")
        return False

def validate_json(path, name):
    """Validate JSON file"""
    try:
        with open(path, 'r') as f:
            json.load(f)
        print(f"  ✅ {name} (valid JSON)")
        return True
    except Exception as e:
        print(f"  ❌ {name} (invalid JSON: {e})")
        return False

def main():
    print("=" * 70)
    print("🚀 DEPLOYMENT READINESS CHECK")
    print("=" * 70)
    print()
    
    all_good = True
    
    # Check deployment config files
    print("📋 DEPLOYMENT CONFIGURATION FILES")
    print("-" * 70)
    all_good &= check_file_exists("render.yaml", "render.yaml (Render config)")
    all_good &= check_file_exists("vercel.json", "vercel.json (Vercel config)")
    all_good &= check_file_exists("Dockerfile", "Dockerfile (Docker image)")
    all_good &= check_file_exists(".dockerignore", ".dockerignore")
    all_good &= check_file_exists("runtime.txt", "runtime.txt (Python version)")
    all_good &= check_file_exists("web/.env.production", ".env.production (Frontend env)")
    print()
    
    # Check deployment documentation
    print("📚 DEPLOYMENT DOCUMENTATION")
    print("-" * 70)
    all_good &= check_file_exists("DEPLOYMENT_PACKAGE_CREATED.md", "Package overview")
    all_good &= check_file_exists("DEPLOYMENT_FREEMIUM_GUIDE.md", "Complete guide")
    all_good &= check_file_exists("DEPLOYMENT_QUICK_START.txt", "Quick start reference")
    all_good &= check_file_exists("DEPLOYMENT_VERIFICATION.md", "Verification checklist")
    print()
    
    # Check backend files
    print("⚙️  BACKEND FILES")
    print("-" * 70)
    all_good &= check_file_exists("ml_api.py", "ML API entry point")
    all_good &= check_file_exists("requirements.txt", "Python dependencies")
    all_good &= check_file_exists("requirements_production.txt", "Production dependencies")
    all_good &= check_directory_exists("ml", "ML module")
    all_good &= check_file_exists("ml/ml_api_service_optimized.py", "Optimized ML API service")
    all_good &= check_file_exists("ml/validation.py", "Input validation")
    print()
    
    # Check models
    print("🧠 TRAINED MODELS")
    print("-" * 70)
    all_good &= check_directory_exists("optimized_models_25000_samples", "Model artifacts")
    if os.path.isdir("optimized_models_25000_samples"):
        all_good &= check_file_exists("optimized_models_25000_samples/gradient_boosting_optimized.pkl", "Gradient Boosting model")
        all_good &= check_file_exists("optimized_models_25000_samples/random_forest_optimized.pkl", "Random Forest model")
        all_good &= check_file_exists("optimized_models_25000_samples/metadata.json", "Model metadata")
    print()
    
    # Check frontend
    print("🎨 FRONTEND")
    print("-" * 70)
    all_good &= check_directory_exists("web", "Web directory")
    all_good &= check_file_exists("web/package.json", "Frontend dependencies")
    all_good &= check_file_exists("web/vite.config.ts", "Vite config")
    all_good &= check_directory_exists("web/src", "Source code")
    print()
    
    # Check database
    print("🗄️  DATABASE")
    print("-" * 70)
    all_good &= check_directory_exists("web/supabase", "Supabase config")
    if os.path.isdir("web/supabase"):
        migrations = len([f for f in os.listdir("web/supabase") if f.endswith(".sql")])
        print(f"  ✅ Database migrations ({migrations} files)")
    print()
    
    # Validate JSON files
    print("✔️  JSON VALIDATION")
    print("-" * 70)
    all_good &= validate_json("vercel.json", "vercel.json")
    all_good &= validate_json("optimized_models_25000_samples/metadata.json", "Model metadata")
    print()
    
    # Summary
    print("=" * 70)
    if all_good:
        print("✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1️⃣  Deploy backend to Render (25 minutes)")
        print("  2️⃣  Get Render URL")
        print("  3️⃣  Update VITE_BACKEND_URL in web/.env.production")
        print("  4️⃣  Deploy frontend to Vercel (10 minutes)")
        print("  5️⃣  Run verification tests")
        print()
        print("Follow: DEPLOYMENT_QUICK_START.txt for copy-paste commands")
        print()
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 70)
        print()
        print("Please fix the issues above before deploying.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""
🧪 COMPREHENSIVE EXPLAINABILITY TESTING
========================================

Tests for SHAP/LIME explanations and API integration
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Add path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all required modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Checking Imports")
    print("="*60)
    
    try:
        print("  📦 Importing numpy...", end=" ")
        import numpy
        print(f"✅ {numpy.__version__}")
        
        print("  📦 Importing pandas...", end=" ")
        import pandas
        print(f"✅ {pandas.__version__}")
        
        print("  📦 Importing sklearn...", end=" ")
        import sklearn
        print(f"✅ {sklearn.__version__}")
        
        print("  📦 Importing shap...", end=" ")
        import shap
        print(f"✅ {shap.__version__}")
        
        print("  📦 Importing lime...", end=" ")
        import lime
        print(f"✅ ")
        
        print("  📦 Importing ExplainabilityService...", end=" ")
        from explainability_service import ExplainabilityService
        print("✅")
        
        print("\n✅ All imports successful!")
        return True
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        return False


def test_service_initialization():
    """Test ExplainabilityService initialization"""
    print("\n" + "="*60)
    print("TEST 2: Service Initialization")
    print("="*60)
    
    try:
        from explainability_service import ExplainabilityService
        
        print("  🚀 Initializing ExplainabilityService...", end=" ")
        service = ExplainabilityService()
        print("✅")
        
        print("  ✔️  Service attributes:")
        print(f"     - explainer_cache: {type(service.explainer_cache)}")
        print(f"     - feature_names: {type(service.feature_names)}")
        
        print("\n✅ Service initialized successfully!")
        return True, service
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        return False, None


def test_shap_explanation():
    """Test SHAP explanation with Random Forest"""
    print("\n" + "="*60)
    print("TEST 3: SHAP Explanation (Random Forest)")
    print("="*60)
    
    try:
        from sklearn.ensemble import RandomForestRegressor
        from explainability_service import ExplainabilityService
        
        # Create synthetic data
        print("  📊 Creating synthetic dataset...", end=" ")
        np.random.seed(42)
        X_train = np.random.rand(100, 5)
        y_train = 100 + 50 * X_train[:, 0] + 30 * X_train[:, 1] + np.random.normal(0, 10, 100)
        
        X_test = np.array([[0.5, 0.3, 0.2, 0.4, 0.1]])
        feature_names = ['feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5']
        print("✅")
        
        # Train model
        print("  🤖 Training Random Forest...", end=" ")
        model = RandomForestRegressor(n_estimators=10, random_state=42, max_depth=5)
        model.fit(X_train, y_train)
        print("✅")
        
        # Create service and explain
        print("  🔍 Generating SHAP explanation...", end=" ")
        service = ExplainabilityService()
        
        X_test_df = pd.DataFrame(X_test, columns=feature_names)
        X_train_df = pd.DataFrame(X_train, columns=feature_names)
        
        explanation = service.explain_vat_prediction(
            model=model,
            input_data=X_test_df,
            feature_names=feature_names,
            model_type="random_forest",
            method="shap"
        )
        print("✅")
        
        # Validate result
        print("  ✔️  Explanation structure:")
        print(f"     - Status: {explanation.get('status')}")
        print(f"     - Method: {explanation.get('method')}")
        print(f"     - Prediction: {explanation.get('prediction')}")
        print(f"     - Base Value: {explanation.get('base_value')}")
        print(f"     - Features: {len(explanation.get('feature_contributions', []))}")
        
        if explanation.get('status') == 'success':
            print("\n✅ SHAP explanation successful!")
            return True
        else:
            print(f"\n❌ SHAP explanation failed: {explanation.get('error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ SHAP test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_lime_explanation():
    """Test LIME explanation"""
    print("\n" + "="*60)
    print("TEST 4: LIME Explanation")
    print("="*60)
    
    try:
        from sklearn.ensemble import RandomForestRegressor
        from explainability_service import ExplainabilityService
        
        # Create synthetic data
        print("  📊 Creating synthetic dataset...", end=" ")
        np.random.seed(42)
        X_train = np.random.rand(100, 5)
        y_train = 100 + 50 * X_train[:, 0] + 30 * X_train[:, 1] + np.random.normal(0, 10, 100)
        
        X_test = np.array([[0.5, 0.3, 0.2, 0.4, 0.1]])
        feature_names = ['feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5']
        print("✅")
        
        # Train model
        print("  🤖 Training Random Forest...", end=" ")
        model = RandomForestRegressor(n_estimators=10, random_state=42, max_depth=5)
        model.fit(X_train, y_train)
        print("✅")
        
        # Create service and explain
        print("  🔍 Generating LIME explanation...", end=" ")
        service = ExplainabilityService()
        
        X_test_df = pd.DataFrame(X_test, columns=feature_names)
        
        explanation = service.explain_vat_prediction(
            model=model,
            input_data=X_test_df,
            feature_names=feature_names,
            model_type="random_forest",
            method="lime",
            num_samples=100
        )
        print("✅")
        
        # Validate result
        print("  ✔️  Explanation structure:")
        print(f"     - Status: {explanation.get('status')}")
        print(f"     - Method: {explanation.get('method')}")
        print(f"     - Prediction: {explanation.get('prediction')}")
        print(f"     - Feature Weights: {len(explanation.get('feature_weights', []))}")
        
        if explanation.get('status') == 'success':
            print("\n✅ LIME explanation successful!")
            return True
        else:
            print(f"\n❌ LIME explanation failed: {explanation.get('error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ LIME test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_format_api_response():
    """Test API response formatting"""
    print("\n" + "="*60)
    print("TEST 5: API Response Formatting")
    print("="*60)
    
    try:
        from explainability_service import format_explanation_for_api
        
        # Create sample explanation
        print("  📦 Creating sample explanation...", end=" ")
        sample_explanation = {
            "status": "success",
            "method": "SHAP",
            "prediction": 12500.50,
            "base_value": 10000.0,
            "feature_contributions": [
                {"feature": "amount", "shap_value": 2000, "importance": 0.8},
                {"feature": "region", "shap_value": 500, "importance": 0.2}
            ]
        }
        print("✅")
        
        # Format for API
        print("  🔄 Formatting for API...", end=" ")
        formatted = format_explanation_for_api(sample_explanation)
        print("✅")
        
        # Validate
        print("  ✔️  Formatted response:")
        print(f"     - Status: {formatted.get('status')}")
        print(f"     - Method: {formatted.get('method')}")
        print(f"     - Timestamp: {formatted.get('timestamp')}")
        print(f"     - Data keys: {list(formatted.get('data', {}).keys())}")
        
        print("\n✅ API formatting successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ API formatting test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🔍"*30)
    print("  EXPLAINABILITY COMPREHENSIVE TEST SUITE")
    print("🔍"*30)
    
    results = {}
    
    # Test 1: Imports
    results['imports'] = test_imports()
    
    # Only continue if imports successful
    if not results['imports']:
        print("\n❌ Cannot proceed - imports failed")
        return results
    
    # Test 2: Service initialization
    init_result, service = test_service_initialization()
    results['initialization'] = init_result
    
    # Test 3: SHAP
    results['shap'] = test_shap_explanation()
    
    # Test 4: LIME
    results['lime'] = test_lime_explanation()
    
    # Test 5: API formatting
    results['api_format'] = test_format_api_response()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"  {status}: {test_name.upper()}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Explainability service is ready.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review above for details.")
    
    return results


if __name__ == "__main__":
    results = main()
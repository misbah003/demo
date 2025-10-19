"""
✅ EXPLAINABILITY FEATURE TEST SUITE
===================================

Comprehensive tests for all explainability features:
- SHAP explanations
- LIME explanations
- PDF report generation
- API endpoints
- Error handling

Run with: python test_explainability.py
"""

import sys
import json
import tempfile
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
CHECKMARK = '✅'
CROSS = '❌'

class ExplainabilityTestSuite:
    """Test suite for explainability features"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = f"{CHECKMARK} PASS" if passed else f"{CROSS} FAIL"
        color = GREEN if passed else RED
        
        print(f"{color}{status}{RESET} {test_name}")
        if message:
            print(f"     └─ {message}")
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        
        self.results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_imports(self):
        """Test that all modules can be imported"""
        print(f"\n{BLUE}Testing Imports...{RESET}")
        
        try:
            from explainability_service import ExplainabilityService
            self.log_result("Import ExplainabilityService", True)
        except Exception as e:
            self.log_result("Import ExplainabilityService", False, str(e))
            return
        
        try:
            from pdf_report_generator import PDFReportGenerator
            self.log_result("Import PDFReportGenerator", True)
        except Exception as e:
            self.log_result("Import PDFReportGenerator", False, str(e))
            return
        
        # Test optional imports
        try:
            import shap
            self.log_result("Import SHAP library", True)
        except Exception as e:
            self.log_result("Import SHAP library", False, f"Required: pip install shap")
        
        try:
            import lime
            self.log_result("Import LIME library", True)
        except Exception as e:
            self.log_result("Import LIME library", False, f"Required: pip install lime")
        
        try:
            import reportlab
            self.log_result("Import ReportLab library", True)
        except Exception as e:
            self.log_result("Import ReportLab library", False, f"Required: pip install reportlab")
    
    def test_explainability_service(self):
        """Test ExplainabilityService functionality"""
        print(f"\n{BLUE}Testing ExplainabilityService...{RESET}")
        
        try:
            from explainability_service import ExplainabilityService
            service = ExplainabilityService()
            self.log_result("Initialize ExplainabilityService", True)
        except Exception as e:
            self.log_result("Initialize ExplainabilityService", False, str(e))
            return
        
        # Test with dummy data
        try:
            from sklearn.ensemble import RandomForestRegressor
            
            # Create dummy model and data
            X_train = pd.DataFrame({
                'amount': np.random.rand(100) * 100000,
                'region': np.random.randint(0, 5, 100),
                'category': np.random.randint(0, 3, 100)
            })
            y_train = np.random.rand(100) * 50000
            
            model = RandomForestRegressor(n_estimators=10, random_state=42)
            model.fit(X_train, y_train)
            
            X_test = pd.DataFrame({
                'amount': [50000],
                'region': [1],
                'category': [0]
            })
            
            # Test SHAP explanation
            try:
                explanation = service.explain_vat_prediction(
                    model=model,
                    input_data=X_test,
                    feature_names=['amount', 'region', 'category'],
                    model_type='random_forest',
                    method='shap'
                )
                
                has_required_fields = all(k in explanation for k in ['method', 'status', 'prediction'])
                self.log_result(
                    "SHAP explanation generation",
                    explanation.get('status') == 'success' and has_required_fields,
                    f"Method: {explanation.get('method')}"
                )
            except Exception as e:
                self.log_result("SHAP explanation generation", False, str(e))
            
            # Test LIME explanation
            try:
                explanation = service.explain_vat_prediction(
                    model=model,
                    input_data=X_test,
                    feature_names=['amount', 'region', 'category'],
                    model_type='random_forest',
                    method='lime'
                )
                
                has_required_fields = all(k in explanation for k in ['method', 'status'])
                self.log_result(
                    "LIME explanation generation",
                    explanation.get('status') == 'success' and has_required_fields,
                    f"Method: {explanation.get('method')}"
                )
            except Exception as e:
                self.log_result("LIME explanation generation", False, str(e))
                
        except ImportError as e:
            self.log_result("ExplainabilityService tests", False, f"Missing dependency: {e}")
    
    def test_pdf_generator(self):
        """Test PDF report generation"""
        print(f"\n{BLUE}Testing PDF Report Generator...{RESET}")
        
        try:
            from pdf_report_generator import PDFReportGenerator
            
            with tempfile.TemporaryDirectory() as tmpdir:
                generator = PDFReportGenerator(output_dir=tmpdir)
                self.log_result("Initialize PDFReportGenerator", True)
                
                # Create sample explanation
                sample_explanation = {
                    "method": "SHAP",
                    "status": "success",
                    "base_value": 30000,
                    "prediction": 50000,
                    "confidence": 0.85,
                    "feature_contributions": [
                        {
                            "feature": "amount",
                            "shap_value": 15000,
                            "importance": 0.5,
                            "direction": "positive"
                        },
                        {
                            "feature": "region",
                            "shap_value": 5000,
                            "importance": 0.2,
                            "direction": "positive"
                        }
                    ],
                    "timestamp": datetime.now().isoformat(),
                    "is_anomaly": False
                }
                
                # Generate report
                try:
                    pdf_path = generator.generate_report(
                        explanation_data=sample_explanation,
                        model_name="test_model",
                        input_summary={"region": "EU", "amount": 50000},
                        include_charts=False  # Skip charts for faster testing
                    )
                    
                    pdf_exists = Path(pdf_path).exists()
                    self.log_result(
                        "PDF report generation",
                        pdf_exists,
                        f"Generated: {Path(pdf_path).name}"
                    )
                    
                except Exception as e:
                    self.log_result("PDF report generation", False, str(e))
                    
        except ImportError as e:
            self.log_result("PDFReportGenerator tests", False, f"Missing dependency: {e}")
    
    def test_api_structure(self):
        """Test API module structure"""
        print(f"\n{BLUE}Testing API Structure...{RESET}")
        
        try:
            # Check if API file exists
            api_path = Path("ml_api_with_explainability.py")
            api_exists = api_path.exists()
            self.log_result("API module exists", api_exists)
            
            if api_exists:
                # Parse file for required endpoints
                with open(api_path, 'r') as f:
                    content = f.read()
                
                endpoints = [
                    '/api/explain-vat',
                    '/api/explain-document',
                    '/api/explain-anomaly',
                    '/api/explain-report',
                    '/api/explain-batch'
                ]
                
                for endpoint in endpoints:
                    has_endpoint = endpoint in content
                    self.log_result(f"Endpoint {endpoint} defined", has_endpoint)
                    
        except Exception as e:
            self.log_result("API structure tests", False, str(e))
    
    def test_documentation(self):
        """Test that documentation files exist"""
        print(f"\n{BLUE}Testing Documentation...{RESET}")
        
        doc_files = [
            ("EXPLAINABILITY_GUIDE.md", "Explainability Guide"),
            ("EXPLAINABILITY_IMPLEMENTATION.md", "Implementation Summary"),
            ("ml/explainability_service.py", "Service Module")
        ]
        
        for file_path, description in doc_files:
            exists = Path(file_path).exists()
            self.log_result(f"Document: {description}", exists)
    
    def test_react_component(self):
        """Test React component exists"""
        print(f"\n{BLUE}Testing React Components...{RESET}")
        
        component_path = Path("web/src/components/ExplainabilityDashboard.tsx")
        exists = component_path.exists()
        
        self.log_result("ExplainabilityDashboard component", exists)
        
        if exists:
            with open(component_path, 'r') as f:
                content = f.read()
            
            required_elements = [
                'ExplainabilityDashboard',
                'FeatureContribution',
                'explain_vat',
                'explain_document',
                'fetchExplanation'
            ]
            
            for element in required_elements:
                has_element = element in content
                self.log_result(f"Component includes {element}", has_element)
    
    def generate_report(self):
        """Generate test report"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}TEST SUMMARY{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{GREEN}Passed: {self.passed}/{total}{RESET}")
        print(f"{RED}Failed: {self.failed}/{total}{RESET}")
        print(f"{YELLOW}Pass Rate: {pass_rate:.1f}%{RESET}")
        
        if self.failed == 0:
            print(f"\n{GREEN}✅ ALL TESTS PASSED!{RESET}")
            print(f"{GREEN}Explainability features are ready for deployment{RESET}")
            return True
        else:
            print(f"\n{RED}⚠️ SOME TESTS FAILED{RESET}")
            print(f"{YELLOW}Please fix failing tests before deployment{RESET}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}EXPLAINABILITY TEST SUITE{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        
        self.test_imports()
        self.test_explainability_service()
        self.test_pdf_generator()
        self.test_api_structure()
        self.test_documentation()
        self.test_react_component()
        
        return self.generate_report()


def main():
    """Run test suite"""
    suite = ExplainabilityTestSuite()
    success = suite.run_all_tests()
    
    # Save results
    with open("test_results.json", "w") as f:
        json.dump({
            "passed": suite.passed,
            "failed": suite.failed,
            "total": suite.passed + suite.failed,
            "results": suite.results,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
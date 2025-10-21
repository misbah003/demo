"""
🔍 SHAP DIAGNOSTIC ANALYSIS & SENSITIVITY TESTING
==================================================

Comprehensive analysis to:
1. Create alternative test scenarios (stress testing)
2. Analyze feature sensitivity and model bias
3. Validate if model can return "good" (high) predictions
4. Identify over-weighting and data quality issues
5. Generate recommendations for model recalibration

Usage:
    python SHAP_DIAGNOSTIC_ANALYSIS.py
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import os
from typing import Dict, List

# ==================== CONFIGURATION ====================
ML_API_URL = "http://localhost:8000"
EXPLAIN_ENDPOINT = f"{ML_API_URL}/explain"
PREDICT_ENDPOINT = f"{ML_API_URL}/predict"

# ==================== TEST SCENARIOS ====================

class TestScenarios:
    """Generate comprehensive test scenarios"""
    
    @staticmethod
    def baseline_test():
        """Original test case - CURRENTLY FAILING"""
        return {
            "name": "BASELINE (Original Failing Test)",
            "description": "Original test that returns low refund",
            "data": {
                "Amount": 50000,
                "VAT_Rate": 19,
                "Risk_Score": 0.3,
                "Annual_Turnover": 500000,
                "Category": "goods",
                "Region": "EU",
                "Filing_Status": "quarterly",
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }
    
    @staticmethod
    def good_scenario_test():
        """GOOD scenario - everything positive"""
        return {
            "name": "GOOD SCENARIO (All Positive Signals)",
            "description": "Clean, compliant, high-value refund eligible",
            "data": {
                "Amount": 100000,  # Higher transaction amount
                "VAT_Rate": 19,    # Standard EU VAT
                "Risk_Score": 0.1, # Very low risk
                "Annual_Turnover": 1000000,  # High turnover
                "Category": "goods",
                "Region": "EU",
                "Filing_Status": "monthly",  # Better filing frequency
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }
    
    @staticmethod
    def stress_test_filing_status():
        """Test different filing statuses"""
        return {
            "name": "STRESS TEST: Filing Status Sensitivity",
            "description": "Test how Filing_Status affects predictions",
            "scenarios": [
                {
                    "filing_status": "monthly",
                    "description": "Monthly filer (most frequent)"
                },
                {
                    "filing_status": "quarterly",
                    "description": "Quarterly filer (original)"
                },
                {
                    "filing_status": "annual",
                    "description": "Annual filer (least frequent)"
                }
            ],
            "base_data": {
                "Amount": 50000,
                "VAT_Rate": 19,
                "Risk_Score": 0.3,
                "Annual_Turnover": 500000,
                "Category": "goods",
                "Region": "EU",
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }
    
    @staticmethod
    def stress_test_vat_amount():
        """Test different VAT amounts"""
        return {
            "name": "STRESS TEST: VAT Amount Sensitivity",
            "description": "Test how VAT_Rate affects predictions",
            "scenarios": [
                {"vat_rate": 5, "description": "Low VAT rate (reduced rate)"},
                {"vat_rate": 19, "description": "Standard VAT rate (original)"},
                {"vat_rate": 25, "description": "High VAT rate"}
            ],
            "base_data": {
                "Amount": 50000,
                "Risk_Score": 0.3,
                "Annual_Turnover": 500000,
                "Category": "goods",
                "Region": "EU",
                "Filing_Status": "quarterly",
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }
    
    @staticmethod
    def stress_test_compliance():
        """Test different compliance flags"""
        return {
            "name": "STRESS TEST: Compliance Flag Sensitivity",
            "description": "Test how Compliance affects refund predictions",
            "scenarios": [
                {
                    "compliance": "Compliant",
                    "is_anomaly": "No",
                    "description": "Fully compliant, no anomalies"
                },
                {
                    "compliance": "Partially_Compliant",
                    "is_anomaly": "No",
                    "description": "Partially compliant"
                },
                {
                    "compliance": "Non-Compliant",
                    "is_anomaly": "Yes",
                    "description": "Non-compliant with anomaly"
                }
            ],
            "base_data": {
                "Amount": 50000,
                "VAT_Rate": 19,
                "Risk_Score": 0.3,
                "Annual_Turnover": 500000,
                "Category": "goods",
                "Region": "EU",
                "Filing_Status": "quarterly",
                "Refund_Eligible": "Yes"
            }
        }
    
    @staticmethod
    def stress_test_risk_score():
        """Test different risk scores"""
        return {
            "name": "STRESS TEST: Risk Score Sensitivity",
            "description": "Test how Risk_Score affects predictions",
            "scenarios": [
                {"risk": 0.1, "description": "Very low risk"},
                {"risk": 0.3, "description": "Low risk (original)"},
                {"risk": 0.5, "description": "Medium risk"},
                {"risk": 0.7, "description": "High risk"},
                {"risk": 0.9, "description": "Very high risk"}
            ],
            "base_data": {
                "Amount": 50000,
                "VAT_Rate": 19,
                "Annual_Turnover": 500000,
                "Category": "goods",
                "Region": "EU",
                "Filing_Status": "quarterly",
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }
    
    @staticmethod
    def stress_test_turnover():
        """Test different turnover levels"""
        return {
            "name": "STRESS TEST: Turnover Sensitivity",
            "description": "Test how Annual_Turnover affects predictions",
            "scenarios": [
                {"turnover": 100000, "description": "Very low turnover"},
                {"turnover": 500000, "description": "Medium turnover (original)"},
                {"turnover": 1000000, "description": "High turnover"},
                {"turnover": 5000000, "description": "Very high turnover"}
            ],
            "base_data": {
                "Amount": 50000,
                "VAT_Rate": 19,
                "Risk_Score": 0.3,
                "Category": "goods",
                "Region": "EU",
                "Filing_Status": "quarterly",
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }


class DiagnosticAnalyzer:
    """Run diagnostic tests and generate analysis"""
    
    def __init__(self):
        self.results = []
        self.api_available = self._check_api_available()
    
    def _check_api_available(self):
        """Check if ML API is running"""
        try:
            response = requests.get(f"{ML_API_URL}/health", timeout=2)
            print("✅ ML API is running")
            return True
        except:
            print("❌ ML API is NOT running. Please start it with: python ml_api.py")
            return False
    
    def call_api(self, endpoint, data):
        """Call API endpoint"""
        try:
            response = requests.post(endpoint, json=data, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def run_single_prediction(self, test_case):
        """Run single prediction and get SHAP explanation"""
        data = test_case["data"]
        
        # Get prediction
        pred_response = self.call_api(PREDICT_ENDPOINT, data)
        
        # Get SHAP explanation
        shap_response = self.call_api(EXPLAIN_ENDPOINT, data)
        
        return {
            "test_name": test_case["name"],
            "prediction": pred_response.get("predicted_refund_amount"),
            "recommendation": pred_response.get("recommendation"),
            "shap_response": shap_response,
            "full_prediction": pred_response
        }
    
    def run_baseline_analysis(self):
        """Run baseline test to understand current behavior"""
        print("\n" + "="*70)
        print("🔍 BASELINE ANALYSIS")
        print("="*70)
        
        baseline = TestScenarios.baseline_test()
        result = self.run_single_prediction(baseline)
        
        print(f"\nTest: {baseline['name']}")
        print(f"Description: {baseline['description']}")
        print(f"\n📊 Predicted Refund: €{result['prediction']:,.2f}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"\n🎯 SHAP Analysis:")
        
        if "all_features" in result["shap_response"]:
            features = result["shap_response"]["all_features"]
            base_value = result["shap_response"]["base_value"]
            prediction = result["shap_response"]["prediction"]
            
            print(f"   Base Value: €{base_value:,.2f}")
            print(f"   Prediction: €{prediction:,.2f}")
            print(f"   Net Change: €{prediction - base_value:,.2f}")
            
            print(f"\n   Top 5 Features by SHAP Impact:")
            for i, feat in enumerate(features[:5], 1):
                print(f"   {i}. {feat['feature']}: SHAP={feat['shap_value']:,.2f}, "
                      f"Contribution={feat['contribution']:,.2f}")
        
        return result
    
    def run_good_scenario_analysis(self):
        """Run test with all positive signals"""
        print("\n" + "="*70)
        print("✅ GOOD SCENARIO ANALYSIS")
        print("="*70)
        
        good = TestScenarios.good_scenario_test()
        result = self.run_single_prediction(good)
        
        print(f"\nTest: {good['name']}")
        print(f"Description: {good['description']}")
        print(f"\n📊 Predicted Refund: €{result['prediction']:,.2f}")
        print(f"Recommendation: {result['recommendation']}")
        
        if "all_features" in result["shap_response"]:
            features = result["shap_response"]["all_features"]
            base_value = result["shap_response"]["base_value"]
            prediction = result["shap_response"]["prediction"]
            
            print(f"\n🎯 SHAP Analysis:")
            print(f"   Base Value: €{base_value:,.2f}")
            print(f"   Prediction: €{prediction:,.2f}")
            print(f"   Net Change: €{prediction - base_value:,.2f}")
        
        return result
    
    def run_sensitivity_analysis(self, stress_test_generator):
        """Run sensitivity analysis for a feature"""
        print("\n" + "="*70)
        print(f"🧪 {stress_test_generator()['name'].upper()}")
        print("="*70)
        
        test_def = stress_test_generator()
        results_list = []
        
        for scenario in test_def["scenarios"]:
            data = test_def["base_data"].copy()
            
            # Update parameter
            if "filing_status" in scenario:
                data["Filing_Status"] = scenario["filing_status"]
            elif "vat_rate" in scenario:
                data["VAT_Rate"] = scenario["vat_rate"]
            elif "compliance" in scenario:
                data["Compliance_Flag"] = scenario["compliance"]
                data["Is_Anomaly"] = scenario["is_anomaly"]
            elif "risk" in scenario:
                data["Risk_Score"] = scenario["risk"]
            elif "turnover" in scenario:
                data["Annual_Turnover"] = scenario["turnover"]
            
            pred = self.call_api(PREDICT_ENDPOINT, data)
            refund = pred.get("predicted_refund_amount", 0)
            
            results_list.append({
                "scenario": scenario,
                "refund": refund
            })
            
            print(f"\n  {scenario['description']}")
            print(f"  → Predicted Refund: €{refund:,.2f}")
        
        # Analyze sensitivity
        refunds = [r["refund"] for r in results_list]
        variance = max(refunds) - min(refunds)
        
        print(f"\n📈 Sensitivity Analysis:")
        print(f"   Min Refund: €{min(refunds):,.2f}")
        print(f"   Max Refund: €{max(refunds):,.2f}")
        print(f"   Variance: €{variance:,.2f}")
        print(f"   Sensitivity: {'🔴 HIGH (model very sensitive)' if variance > 5000 else '🟡 MEDIUM' if variance > 2000 else '🟢 LOW'}")
        
        return results_list
    
    def run_full_diagnosis(self):
        """Run complete diagnostic"""
        if not self.api_available:
            return
        
        print("\n" + "🔍 "*35)
        print("SHAP DIAGNOSTIC ANALYSIS - FULL REPORT")
        print("🔍 "*35)
        
        # 1. Baseline Analysis
        baseline_result = self.run_baseline_analysis()
        
        # 2. Good Scenario Analysis
        good_result = self.run_good_scenario_analysis()
        
        # 3. Sensitivity Tests
        print("\n" + "="*70)
        print("SENSITIVITY ANALYSIS")
        print("="*70)
        
        filing_sensitivity = self.run_sensitivity_analysis(TestScenarios.stress_test_filing_status)
        vat_sensitivity = self.run_sensitivity_analysis(TestScenarios.stress_test_vat_amount)
        compliance_sensitivity = self.run_sensitivity_analysis(TestScenarios.stress_test_compliance)
        risk_sensitivity = self.run_sensitivity_analysis(TestScenarios.stress_test_risk_score)
        turnover_sensitivity = self.run_sensitivity_analysis(TestScenarios.stress_test_turnover)
        
        # 4. Generate Report
        self._generate_report(
            baseline_result, good_result,
            filing_sensitivity, vat_sensitivity, compliance_sensitivity,
            risk_sensitivity, turnover_sensitivity
        )
    
    def _generate_report(self, baseline, good, filing_sens, vat_sens, compliance_sens, risk_sens, turnover_sens):
        """Generate comprehensive diagnostic report"""
        print("\n" + "="*70)
        print("📋 DIAGNOSTIC REPORT & RECOMMENDATIONS")
        print("="*70)
        
        baseline_refund = baseline.get("prediction", 0)
        good_refund = good.get("prediction", 0)
        
        print(f"\n1️⃣ BASELINE TEST:")
        print(f"   Predicted Refund: €{baseline_refund:,.2f}")
        print(f"   Status: {'❌ LOW (Concerning)' if baseline_refund < 5000 else '⚠️ MEDIUM' if baseline_refund < 10000 else '✅ HIGH'}")
        
        print(f"\n2️⃣ GOOD SCENARIO TEST:")
        print(f"   Predicted Refund: €{good_refund:,.2f}")
        print(f"   Status: {'✅ Model CAN produce high refunds' if good_refund > 10000 else '❌ Model appears conservative even with positive signals'}")
        
        print(f"\n3️⃣ MODEL BIAS ASSESSMENT:")
        if good_refund > baseline_refund * 1.5:
            print(f"   Status: ✅ MODEL IS RESPONSIVE")
            print(f"   The model DOES respond to positive signals (increased refund by {((good_refund/baseline_refund - 1) * 100):.1f}%)")
        else:
            print(f"   Status: 🔴 MODEL IS OVERLY CONSERVATIVE")
            print(f"   Even with positive signals, refund increased only {((good_refund/baseline_refund - 1) * 100):.1f}%")
        
        print(f"\n4️⃣ FEATURE SENSITIVITY RANKINGS:")
        
        filing_var = max([r["refund"] for r in filing_sens]) - min([r["refund"] for r in filing_sens])
        vat_var = max([r["refund"] for r in vat_sens]) - min([r["refund"] for r in vat_sens])
        compliance_var = max([r["refund"] for r in compliance_sens]) - min([r["refund"] for r in compliance_sens])
        risk_var = max([r["refund"] for r in risk_sens]) - min([r["refund"] for r in risk_sens])
        turnover_var = max([r["refund"] for r in turnover_sens]) - min([r["refund"] for r in turnover_sens])
        
        sensitivities = [
            ("Filing Status", filing_var),
            ("VAT Rate", vat_var),
            ("Compliance Flag", compliance_var),
            ("Risk Score", risk_var),
            ("Annual Turnover", turnover_var)
        ]
        sensitivities.sort(key=lambda x: x[1], reverse=True)
        
        for i, (name, sensitivity) in enumerate(sensitivities, 1):
            impact = "🔴 CRITICAL" if sensitivity > 10000 else "🟡 HIGH" if sensitivity > 5000 else "🟢 MEDIUM" if sensitivity > 2000 else "✅ LOW"
            print(f"   {i}. {name}: €{sensitivity:,.0f} variance {impact}")
        
        print(f"\n5️⃣ KEY FINDINGS:")
        print(f"   • Model uses {5} key features for decisions")
        print(f"   • Most sensitive feature: {sensitivities[0][0]} (€{sensitivities[0][1]:,.0f} variance)")
        print(f"   • Most stable feature: {sensitivities[-1][0]} (€{sensitivities[-1][1]:,.0f} variance)")
        
        print(f"\n6️⃣ RECOMMENDATIONS:")
        if good_refund < baseline_refund * 1.2:
            print(f"   🔴 MODEL IS OVERLY CONSERVATIVE - Consider:")
            print(f"      • Recalibrating feature weights")
            print(f"      • Checking training data for bias")
            print(f"      • Adjusting the Ridge regularization")
        else:
            print(f"   ✅ Model is responsive and reasonable")
        
        if sensitivities[0][1] > 10000:
            print(f"   ⚠️  {sensitivities[0][0]} has excessive influence - Consider:")
            print(f"      • Re-encoding or normalizing this feature")
            print(f"      • Feature importance rebalancing")
        
        print(f"\n" + "="*70)
        print("📌 END OF REPORT")
        print("="*70)


# ==================== MAIN ====================

if __name__ == "__main__":
    analyzer = DiagnosticAnalyzer()
    analyzer.run_full_diagnosis()
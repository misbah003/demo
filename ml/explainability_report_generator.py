"""
📄 EXPLAINABILITY REPORT GENERATOR
===================================

Generates comprehensive explainability reports in JSON, HTML, and PDF formats
with SHAP values, feature importance, and predictions.

Features:
- Multi-format support (JSON, HTML, PDF)
- Professional report styling
- Feature importance charts
- SHAP value visualization
- Risk assessment summaries
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

# For PDF generation
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    logging.warning("⚠️  reportlab not installed. PDF generation will be limited.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainabilityReportGenerator:
    """Generate comprehensive explainability reports"""
    
    def __init__(self, output_dir: str = 'explainability_reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Report generator initialized. Output: {self.output_dir}")
    
    # ==================== JSON REPORTS ====================
    
    def generate_json_report(
        self,
        prediction_data: Dict[str, Any],
        explanation_data: Dict[str, Any],
        model_name: str,
        model_type: str = "vat_predictor"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive JSON report
        
        Args:
            prediction_data: Original prediction input
            explanation_data: SHAP/LIME explanation output
            model_name: Name of the model
            model_type: Type of model (vat_predictor, document_classifier, etc.)
            
        Returns:
            Dictionary with report data
        """
        try:
            report = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "model_name": model_name,
                    "model_type": model_type,
                    "report_version": "1.0"
                },
                "prediction": {
                    "value": explanation_data.get('prediction'),
                    "confidence": explanation_data.get('confidence'),
                    "base_value": explanation_data.get('base_value'),
                    "method": explanation_data.get('method')
                },
                "feature_importance": {
                    "top_features": self._extract_top_features(explanation_data, top_n=10),
                    "all_features": explanation_data.get('feature_contributions', []),
                    "feature_count": len(explanation_data.get('feature_contributions', []))
                },
                "risk_assessment": self._assess_risk(explanation_data),
                "interpretation": self._generate_interpretation(explanation_data, model_type),
                "input_data": prediction_data
            }
            
            logger.info(f"✅ JSON report generated for {model_name}")
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating JSON report: {e}")
            return {"error": str(e), "status": "failed"}
    
    # ==================== HTML REPORTS ====================
    
    def generate_html_report(
        self,
        prediction_data: Dict[str, Any],
        explanation_data: Dict[str, Any],
        model_name: str,
        model_type: str = "vat_predictor"
    ) -> str:
        """
        Generate professional HTML report
        
        Args:
            prediction_data: Original prediction input
            explanation_data: SHAP/LIME explanation output
            model_name: Name of the model
            model_type: Type of model
            
        Returns:
            HTML string
        """
        try:
            json_report = self.generate_json_report(
                prediction_data, explanation_data, model_name, model_type
            )
            
            top_features = json_report['feature_importance']['top_features']
            risk_data = json_report['risk_assessment']
            interpretation = json_report['interpretation']
            
            html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explainability Report - {model_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .header {{
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 28px;
            color: #007bff;
            margin-bottom: 10px;
        }}
        
        .metadata {{
            font-size: 12px;
            color: #666;
        }}
        
        .section {{
            margin-bottom: 30px;
            page-break-inside: avoid;
        }}
        
        .section h2 {{
            font-size: 20px;
            color: #007bff;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        
        .prediction-summary {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
        
        .metric-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
        }}
        
        .feature-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .feature-table th {{
            background: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .feature-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        .feature-table tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        .feature-name {{
            font-weight: 500;
            color: #333;
        }}
        
        .importance-bar {{
            display: inline-block;
            height: 20px;
            background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
            border-radius: 3px;
            min-width: 50px;
            text-align: center;
            color: white;
            font-size: 11px;
            line-height: 20px;
            margin-right: 10px;
        }}
        
        .positive {{
            color: #28a745;
            font-weight: 600;
        }}
        
        .negative {{
            color: #dc3545;
            font-weight: 600;
        }}
        
        .risk-badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .risk-high {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .risk-medium {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .risk-low {{
            background: #d4edda;
            color: #155724;
        }}
        
        .interpretation {{
            background: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
            margin-top: 15px;
        }}
        
        .interpretation-item {{
            margin-bottom: 10px;
            padding-left: 20px;
            position: relative;
        }}
        
        .interpretation-item:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #007bff;
            font-weight: bold;
        }}
        
        .footer {{
            border-top: 1px solid #ddd;
            padding-top: 20px;
            margin-top: 30px;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
                padding: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔍 Model Explainability Report</h1>
            <div class="metadata">
                <p><strong>Model:</strong> {model_name} ({model_type})</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Method:</strong> {explanation_data.get('method', 'SHAP')}</p>
            </div>
        </div>
        
        <!-- Prediction Summary -->
        <div class="section">
            <h2>📊 Prediction Summary</h2>
            <div class="prediction-summary">
                <div class="metric-card">
                    <div class="metric-label">Predicted Value</div>
                    <div class="metric-value">{self._format_value(json_report['prediction']['value'])}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value">{json_report['prediction']['confidence'] * 100:.1f}%</div>
                </div>
            </div>
            {f'<p><strong>Base Value (Model Expectation):</strong> {self._format_value(json_report["prediction"]["base_value"])}</p>' if json_report['prediction'].get('base_value') else ''}
        </div>
        
        <!-- Risk Assessment -->
        <div class="section">
            <h2>⚠️ Risk Assessment</h2>
            <p><strong>Risk Level:</strong> <span class="risk-badge risk-{risk_data['level'].lower()}">{risk_data['level']}</span></p>
            <p><strong>Risk Score:</strong> {risk_data['score']:.2f}/100</p>
            <p><strong>Assessment:</strong> {risk_data['assessment']}</p>
        </div>
        
        <!-- Top Features -->
        <div class="section">
            <h2>🎯 Top Contributing Features</h2>
            <table class="feature-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Importance</th>
                        <th>Value</th>
                        <th>Direction</th>
                        <th>SHAP Value</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_feature_rows(top_features)}
                </tbody>
            </table>
        </div>
        
        <!-- Interpretation -->
        <div class="section">
            <h2>💡 Interpretation</h2>
            <div class="interpretation">
                {self._generate_interpretation_html(interpretation)}
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>This report provides model explainability insights using SHAP (SHapley Additive exPlanations) and/or LIME (Local Interpretable Model-agnostic Explanations).</p>
            <p>For more information, visit: <a href="https://github.com/slundberg/shap">SHAP Documentation</a></p>
        </div>
    </div>
</body>
</html>
"""
            logger.info(f"✅ HTML report generated for {model_name}")
            return html
            
        except Exception as e:
            logger.error(f"❌ Error generating HTML report: {e}")
            return f"<p>Error generating report: {e}</p>"
    
    # ==================== PDF REPORTS ====================
    
    def generate_pdf_report(
        self,
        prediction_data: Dict[str, Any],
        explanation_data: Dict[str, Any],
        model_name: str,
        model_type: str = "vat_predictor",
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate PDF report (requires reportlab)
        
        Returns:
            Path to generated PDF or None if reportlab not available
        """
        if not HAS_REPORTLAB:
            logger.warning("⚠️  reportlab not installed. Use HTML report instead.")
            return None
        
        try:
            json_report = self.generate_json_report(
                prediction_data, explanation_data, model_name, model_type
            )
            
            if filename is None:
                filename = f"report_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            filepath = self.output_dir / filename
            
            # Create PDF
            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#007bff'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            # Title
            title = Paragraph(f"🔍 Explainability Report - {model_name}", title_style)
            story.append(title)
            story.append(Spacer(1, 0.3*inch))
            
            # Metadata
            metadata_style = ParagraphStyle(
                'Metadata',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#666')
            )
            metadata_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Model: {model_type} | Method: {explanation_data.get('method', 'SHAP')}"
            story.append(Paragraph(metadata_text, metadata_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Prediction Summary
            story.append(Paragraph("Prediction Summary", styles['Heading2']))
            pred_data = [
                ["Metric", "Value"],
                ["Predicted Value", str(self._format_value(json_report['prediction']['value']))],
                ["Confidence", f"{json_report['prediction']['confidence'] * 100:.1f}%"],
                ["Base Value", str(self._format_value(json_report['prediction'].get('base_value', 'N/A')))],
            ]
            pred_table = Table(pred_data, colWidths=[3*inch, 3*inch])
            pred_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(pred_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Risk Assessment
            risk_data = json_report['risk_assessment']
            story.append(Paragraph("Risk Assessment", styles['Heading2']))
            risk_text = f"<b>Risk Level:</b> {risk_data['level']} | <b>Score:</b> {risk_data['score']:.2f}/100<br/><b>Assessment:</b> {risk_data['assessment']}"
            story.append(Paragraph(risk_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Top Features
            story.append(Paragraph("Top Contributing Features", styles['Heading2']))
            features_data = [["Feature", "Importance", "Direction", "SHAP Value"]]
            for feat in json_report['feature_importance']['top_features'][:10]:
                direction = "📈 Positive" if feat.get('direction') == 'positive' else "📉 Negative"
                features_data.append([
                    feat.get('feature', 'N/A'),
                    f"{feat.get('importance', 0):.4f}",
                    direction,
                    f"{feat.get('shap_value', 0):.4f}"
                ])
            
            features_table = Table(features_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            features_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(features_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Build PDF
            doc.build(story)
            logger.info(f"✅ PDF report generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Error generating PDF report: {e}")
            return None
    
    # ==================== HELPER METHODS ====================
    
    def _extract_top_features(self, explanation_data: Dict, top_n: int = 10) -> List[Dict]:
        """Extract top N features by importance"""
        features = explanation_data.get('feature_contributions', [])
        sorted_features = sorted(
            features,
            key=lambda x: abs(x.get('importance', 0)),
            reverse=True
        )
        return sorted_features[:top_n]
    
    def _assess_risk(self, explanation_data: Dict) -> Dict:
        """Assess prediction risk level"""
        confidence = explanation_data.get('confidence', 0.5)
        is_anomaly = explanation_data.get('is_anomaly', False)
        
        # Calculate risk score
        risk_score = 0
        if is_anomaly:
            risk_score += 50
        
        risk_score += (1 - confidence) * 50
        
        # Determine risk level
        if risk_score >= 70:
            level = "HIGH"
            assessment = "⚠️ High risk detected. Review prediction carefully."
        elif risk_score >= 40:
            level = "MEDIUM"
            assessment = "⚠️ Moderate risk detected. Proceed with caution."
        else:
            level = "LOW"
            assessment = "✅ Low risk. Prediction appears reliable."
        
        return {
            "level": level,
            "score": risk_score,
            "assessment": assessment
        }
    
    def _generate_interpretation(self, explanation_data: Dict, model_type: str) -> List[str]:
        """Generate human-readable interpretation"""
        interpretations = []
        
        # Feature-based interpretation
        top_feature = self._extract_top_features(explanation_data, top_n=1)
        if top_feature:
            feat = top_feature[0]
            direction = "increased" if feat.get('direction') == 'positive' else "decreased"
            interpretations.append(
                f"The prediction was {direction} primarily by '{feat.get('feature', 'unknown')}' "
                f"(importance: {feat.get('importance', 0):.4f})"
            )
        
        # Confidence interpretation
        confidence = explanation_data.get('confidence', 0.5)
        if confidence > 0.8:
            interpretations.append("The model shows high confidence in this prediction.")
        elif confidence > 0.5:
            interpretations.append("The model shows moderate confidence in this prediction.")
        else:
            interpretations.append("The model shows low confidence in this prediction. Use with caution.")
        
        # Anomaly interpretation
        if explanation_data.get('is_anomaly'):
            interpretations.append("⚠️ This prediction appears to be an anomaly. Review input data carefully.")
        
        return interpretations
    
    def _format_value(self, value: Any) -> str:
        """Format value for display"""
        if value is None:
            return "N/A"
        if isinstance(value, float):
            return f"€{value:,.2f}" if isinstance(value, (int, float)) else str(value)
        return str(value)
    
    def _generate_feature_rows(self, features: List[Dict]) -> str:
        """Generate HTML table rows for features"""
        rows = ""
        for feat in features:
            direction_icon = "📈" if feat.get('direction') == 'positive' else "📉"
            rows += f"""
            <tr>
                <td class="feature-name">{feat.get('feature', 'N/A')}</td>
                <td>
                    <div class="importance-bar" style="width: {min(feat.get('importance', 0) * 200, 200)}px;">
                        {feat.get('importance', 0):.4f}
                    </div>
                </td>
                <td>{self._format_value(feat.get('value'))}</td>
                <td class="{'positive' if feat.get('direction') == 'positive' else 'negative'}">
                    {direction_icon} {feat.get('direction', 'N/A')}
                </td>
                <td class="{'positive' if feat.get('shap_value', 0) > 0 else 'negative'}">
                    {feat.get('shap_value', 0):.4f}
                </td>
            </tr>
            """
        return rows
    
    def _generate_interpretation_html(self, interpretations: List[str]) -> str:
        """Generate HTML interpretation items"""
        items = ""
        for interp in interpretations:
            items += f'<div class="interpretation-item">{interp}</div>'
        return items
    
    # ==================== FILE OPERATIONS ====================
    
    def save_json_report(
        self,
        prediction_data: Dict[str, Any],
        explanation_data: Dict[str, Any],
        model_name: str,
        model_type: str = "vat_predictor",
        filename: Optional[str] = None
    ) -> str:
        """Save JSON report to file"""
        report = self.generate_json_report(
            prediction_data, explanation_data, model_name, model_type
        )
        
        if filename is None:
            filename = f"report_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"✅ JSON report saved: {filepath}")
        return str(filepath)
    
    def save_html_report(
        self,
        prediction_data: Dict[str, Any],
        explanation_data: Dict[str, Any],
        model_name: str,
        model_type: str = "vat_predictor",
        filename: Optional[str] = None
    ) -> str:
        """Save HTML report to file"""
        html = self.generate_html_report(
            prediction_data, explanation_data, model_name, model_type
        )
        
        if filename is None:
            filename = f"report_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        logger.info(f"✅ HTML report saved: {filepath}")
        return str(filepath)


# ==================== UTILITY FUNCTIONS ====================

def create_report_summary(report_path: str) -> Dict[str, Any]:
    """Create summary of generated report"""
    try:
        with open(report_path, 'r') as f:
            if report_path.endswith('.json'):
                report = json.load(f)
                return {
                    "status": "success",
                    "type": "json",
                    "model": report['metadata']['model_name'],
                    "timestamp": report['metadata']['timestamp'],
                    "path": report_path
                }
    except Exception as e:
        logger.error(f"❌ Error creating report summary: {e}")
        return {"status": "failed", "error": str(e)}


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = ExplainabilityReportGenerator()
    
    # Sample data
    sample_prediction = {"amount": 5000, "frequency": "monthly"}
    sample_explanation = {
        "prediction": 450.50,
        "confidence": 0.85,
        "base_value": 400,
        "method": "SHAP",
        "feature_contributions": [
            {"feature": "amount", "importance": 0.6, "shap_value": 0.45, "value": 5000, "direction": "positive"},
            {"feature": "frequency", "importance": 0.3, "shap_value": 0.05, "value": 12, "direction": "positive"},
            {"feature": "risk_factor", "importance": 0.1, "shap_value": 0.0, "value": 0.1, "direction": "negative"},
        ]
    }
    
    # Generate reports
    json_path = generator.save_json_report(sample_prediction, sample_explanation, "test_model", "vat_predictor")
    html_path = generator.save_html_report(sample_prediction, sample_explanation, "test_model", "vat_predictor")
    pdf_path = generator.generate_pdf_report(sample_prediction, sample_explanation, "test_model", "vat_predictor")
    
    print(f"\n✅ Reports generated:")
    print(f"   JSON: {json_path}")
    print(f"   HTML: {html_path}")
    if pdf_path:
        print(f"   PDF: {pdf_path}")
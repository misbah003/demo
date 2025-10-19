"""
📄 PDF REPORT GENERATOR
======================

Generates downloadable PDF reports from model explanations
Includes:
- Feature importance charts
- Prediction breakdown
- Risk assessment
- Recommendations

Usage:
    from pdf_report_generator import PDFReportGenerator
    generator = PDFReportGenerator()
    pdf_path = generator.generate_report(explanation_data)
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """Generate PDF reports from model explanations"""
    
    def __init__(self, output_dir: str = "explainability_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        logger.info(f"✅ PDF Report Generator initialized")
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['BodyText'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT
        ))
    
    def generate_report(
        self,
        explanation_data: Dict,
        model_name: str = "ML Model",
        input_summary: Optional[Dict] = None,
        include_charts: bool = True
    ) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            explanation_data: Explanation dictionary from ExplainabilityService
            model_name: Name of the model
            input_summary: Summary of input data
            include_charts: Whether to include charts
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Create PDF filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_path = self.output_dir / f"explanation_{model_name}_{timestamp}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(pdf_path),
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Build content
            story = []
            story.extend(self._build_title(model_name))
            story.append(Spacer(1, 0.2*inch))
            
            story.extend(self._build_metadata(explanation_data))
            story.append(Spacer(1, 0.2*inch))
            
            story.extend(self._build_summary(explanation_data, input_summary))
            story.append(Spacer(1, 0.2*inch))
            
            story.extend(self._build_features_section(explanation_data, include_charts))
            story.append(Spacer(1, 0.2*inch))
            
            story.extend(self._build_insights(explanation_data))
            story.append(Spacer(1, 0.2*inch))
            
            story.extend(self._build_recommendations(explanation_data, model_name))
            
            # Build PDF
            doc.build(story)
            logger.info(f"✅ Report generated: {pdf_path}")
            
            return str(pdf_path)
            
        except Exception as e:
            logger.error(f"❌ Error generating report: {e}")
            raise
    
    def _build_title(self, model_name: str) -> List:
        """Build title section"""
        title = Paragraph(
            f"Model Explanation Report<br/>{model_name}",
            self.styles['CustomTitle']
        )
        
        generated_date = Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        )
        
        return [title, generated_date]
    
    def _build_metadata(self, explanation_data: Dict) -> List:
        """Build metadata section"""
        elements = []
        
        metadata_title = Paragraph("Report Information", self.styles['SectionTitle'])
        elements.append(metadata_title)
        
        # Create metadata table
        metadata_items = [
            ["Field", "Value"],
            ["Method", explanation_data.get("method", "Unknown")],
            ["Status", explanation_data.get("status", "Unknown")],
            ["Timestamp", explanation_data.get("timestamp", "Unknown")],
        ]
        
        if "confidence" in explanation_data:
            confidence = explanation_data.get("confidence", 0) * 100
            metadata_items.append(["Confidence", f"{confidence:.1f}%"])
        
        metadata_table = Table(metadata_items, colWidths=[2.5*inch, 3.5*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(metadata_table)
        return elements
    
    def _build_summary(
        self,
        explanation_data: Dict,
        input_summary: Optional[Dict]
    ) -> List:
        """Build prediction summary section"""
        elements = []
        
        summary_title = Paragraph("Prediction Summary", self.styles['SectionTitle'])
        elements.append(summary_title)
        
        # Prediction value
        if "prediction" in explanation_data:
            pred_text = f"<b>Predicted Value:</b> {self._format_value(explanation_data['prediction'])}"
            elements.append(Paragraph(pred_text, self.styles['BodyText']))
        
        # Base value
        if "base_value" in explanation_data:
            base_text = f"<b>Base Value (Expected):</b> {self._format_value(explanation_data['base_value'])}"
            elements.append(Paragraph(base_text, self.styles['BodyText']))
        
        # Difference
        if "prediction" in explanation_data and "base_value" in explanation_data:
            diff = explanation_data['prediction'] - explanation_data['base_value']
            diff_dir = "increase" if diff > 0 else "decrease"
            diff_text = f"<b>Impact:</b> {diff_dir} of {self._format_value(abs(diff))}"
            elements.append(Paragraph(diff_text, self.styles['BodyText']))
        
        # Input summary
        if input_summary:
            elements.append(Spacer(1, 0.1*inch))
            input_title = Paragraph("<b>Input Parameters:</b>", self.styles['Normal'])
            elements.append(input_title)
            
            for key, value in input_summary.items():
                param_text = f"• <b>{key}:</b> {value}"
                elements.append(Paragraph(param_text, self.styles['Normal']))
        
        return elements
    
    def _build_features_section(self, explanation_data: Dict, include_charts: bool) -> List:
        """Build feature importance section"""
        elements = []
        
        if "feature_contributions" not in explanation_data:
            return elements
        
        features_title = Paragraph("Feature Importance", self.styles['SectionTitle'])
        elements.append(features_title)
        
        features = explanation_data["feature_contributions"][:10]  # Top 10
        
        # Create chart if requested
        if include_charts and features:
            try:
                chart_path = self._create_feature_chart(features)
                chart_img = Image(chart_path, width=6*inch, height=3*inch)
                elements.append(chart_img)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                logger.warning(f"Could not create chart: {e}")
        
        # Create feature table
        feature_data = [["Feature", "SHAP Value", "Importance", "Direction"]]
        for feat in features:
            feature_data.append([
                feat.get("feature", "Unknown")[:30],
                f"{feat.get('shap_value', 0):.4f}",
                f"{feat.get('importance', 0):.4f}",
                feat.get("direction", "neutral")
            ])
        
        feature_table = Table(feature_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(feature_table)
        return elements
    
    def _build_insights(self, explanation_data: Dict) -> List:
        """Build insights section"""
        elements = []
        
        insights_title = Paragraph("Key Insights", self.styles['SectionTitle'])
        elements.append(insights_title)
        
        # Generate insights
        insights = self._generate_insights(explanation_data)
        
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", self.styles['BodyText']))
        
        if not insights:
            elements.append(Paragraph("No specific insights available.", self.styles['BodyText']))
        
        return elements
    
    def _build_recommendations(self, explanation_data: Dict, model_name: str) -> List:
        """Build recommendations section"""
        elements = []
        
        rec_title = Paragraph("Recommendations", self.styles['SectionTitle'])
        elements.append(rec_title)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(explanation_data, model_name)
        
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.styles['BodyText']))
        
        if not recommendations:
            elements.append(Paragraph("No specific recommendations at this time.", self.styles['BodyText']))
        
        return elements
    
    def _create_feature_chart(self, features: List[Dict]) -> str:
        """Create feature importance chart"""
        try:
            # Extract data
            names = [f["feature"][:20] for f in features]
            values = [abs(f["shap_value"]) for f in features]
            colors_list = ['#ef4444' if f["direction"] == "negative" else '#22c55e' for f in features]
            
            # Create chart
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(names, values, color=colors_list)
            ax.set_xlabel('SHAP Value (Absolute)')
            ax.set_title('Top Features by Importance')
            ax.invert_yaxis()
            
            # Save chart
            chart_path = self.output_dir / f"feature_chart_{datetime.now().timestamp()}.png"
            plt.savefig(str(chart_path), dpi=100, bbox_inches='tight')
            plt.close()
            
            return str(chart_path)
        except Exception as e:
            logger.error(f"Error creating chart: {e}")
            raise
    
    def _generate_insights(self, explanation_data: Dict) -> List[str]:
        """Generate human-readable insights"""
        insights = []
        
        if explanation_data.get("status") != "success":
            return insights
        
        # Feature insights
        if "feature_contributions" in explanation_data and explanation_data["feature_contributions"]:
            top_feature = explanation_data["feature_contributions"][0]
            insights.append(
                f"Most influential factor: {top_feature['feature']} "
                f"({top_feature['direction']} impact)"
            )
        
        # Confidence insights
        if "confidence" in explanation_data:
            conf = explanation_data["confidence"]
            if conf > 0.9:
                insights.append("High confidence prediction - suitable for automation")
            elif conf < 0.6:
                insights.append("Low confidence - recommend manual verification")
        
        # Anomaly insights
        if explanation_data.get("is_anomaly"):
            insights.append("⚠️ Anomalous pattern detected - recommend compliance review")
        
        return insights
    
    def _generate_recommendations(self, explanation_data: Dict, model_name: str) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if explanation_data.get("status") != "success":
            recommendations.append("Re-run analysis with different parameters")
            return recommendations
        
        # Model-specific recommendations
        if "vat" in model_name.lower():
            if explanation_data.get("prediction", 0) > 50000:
                recommendations.append("Large refund amount - verify supporting documentation")
            recommendations.append("Review top contributing factors before approval")
        
        elif "document" in model_name.lower():
            if explanation_data.get("confidence", 0) < 0.75:
                recommendations.append("Manual document review recommended")
        
        elif "anomaly" in model_name.lower():
            if explanation_data.get("is_anomaly"):
                recommendations.append("Flag for compliance review")
        
        # General recommendations
        recommendations.append("Keep audit trail of this explanation for compliance")
        
        return recommendations
    
    def _format_value(self, value) -> str:
        """Format value for display"""
        if isinstance(value, (int, float)):
            return f"€{value:,.2f}"
        return str(value)


# ===================== UTILITY FUNCTIONS =====================

def generate_batch_reports(
    explanations: List[Dict],
    model_name: str,
    output_dir: str = "explainability_reports"
) -> List[str]:
    """Generate multiple PDF reports"""
    generator = PDFReportGenerator(output_dir)
    paths = []
    
    for i, exp in enumerate(explanations):
        try:
            path = generator.generate_report(
                explanation_data=exp,
                model_name=f"{model_name}_{i}"
            )
            paths.append(path)
        except Exception as e:
            logger.error(f"Error generating report {i}: {e}")
    
    return paths


if __name__ == "__main__":
    # Test the generator
    sample_explanation = {
        "method": "SHAP",
        "status": "success",
        "base_value": 30000,
        "prediction": 50000,
        "confidence": 0.85,
        "feature_contributions": [
            {"feature": "amount", "shap_value": 15000, "importance": 0.5, "direction": "positive"},
            {"feature": "region", "shap_value": 5000, "importance": 0.2, "direction": "positive"},
            {"feature": "category", "shap_value": 3000, "importance": 0.1, "direction": "negative"},
        ],
        "timestamp": datetime.now().isoformat(),
        "is_anomaly": False
    }
    
    generator = PDFReportGenerator()
    path = generator.generate_report(sample_explanation, "test_model")
    print(f"✅ Report generated: {path}")
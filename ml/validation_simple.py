from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Literal, Optional
import logging

logger = logging.getLogger(__name__)

# Valid category values from training data
VALID_FILING_STATUS = {"On Time", "Late", "Very Late"}
VALID_COMPLIANCE_FLAG = {"Compliant", "Non-Compliant", "Under Review"}
VALID_REFUND_ELIGIBLE = {"Yes", "No"}
VALID_IS_ANOMALY = {"Yes", "No"}
VALID_REGIONS = {"East", "North", "South", "West"}
VALID_CATEGORIES = {
    "Retail", "Manufacturing", "Hospitality", "IT Services",
    "Pharmaceuticals", "Healthcare", "Education", "FMCG", "Real Estate", "Others"
}


class PredictionRequest(BaseModel):
    """
    Schema for /predict endpoint requests.
    """
    # Required fields
    Amount: float = Field(..., description="VAT refund amount requested")
    VAT_Rate: float = Field(..., description="VAT rate percentage")
    Risk_Score: float = Field(..., description="Risk assessment score")
    Annual_Turnover: float = Field(..., description="Annual turnover")

    # Categorical fields with strict validation
    Category: str = Field(..., description="Product/Service category")
    Region: str = Field(..., description="Geographic region")
    Filing_Status: str = Field(..., description="Filing status")
    Compliance_Flag: str = Field(..., description="Compliance status")
    Refund_Eligible: str = Field(..., description="Refund eligibility")
    Is_Anomaly: str = Field(..., description="Anomaly flag")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Amount": 50000,
                "VAT_Rate": 19,
                "Risk_Score": 0.3,
                "Annual_Turnover": 500000,
                "Category": "Retail",
                "Region": "East",
                "Filing_Status": "On Time",
                "Compliance_Flag": "Compliant",
                "Refund_Eligible": "Yes",
                "Is_Anomaly": "No"
            }
        }
    )

    @field_validator('Category')
    @classmethod
    def validate_category(cls, v):
        """Validate category is in allowed set"""
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid Category: '{v}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
            )
        return v

    @field_validator('Region')
    @classmethod
    def validate_region(cls, v):
        """Validate region is in allowed set"""
        if v not in VALID_REGIONS:
            raise ValueError(
                f"Invalid Region: '{v}'. Must be one of: {', '.join(sorted(VALID_REGIONS))}"
            )
        return v

    @field_validator('Filing_Status')
    @classmethod
    def validate_filing_status(cls, v):
        """Validate filing status is in allowed set"""
        if v not in VALID_FILING_STATUS:
            raise ValueError(
                f"Invalid Filing_Status: '{v}'. Must be one of: {', '.join(sorted(VALID_FILING_STATUS))}"
            )
        return v

    @field_validator('Compliance_Flag')
    @classmethod
    def validate_compliance_flag(cls, v):
        """Validate compliance flag is in allowed set"""
        if v not in VALID_COMPLIANCE_FLAG:
            raise ValueError(
                f"Invalid Compliance_Flag: '{v}'. Must be one of: {', '.join(sorted(VALID_COMPLIANCE_FLAG))}"
            )
        return v

    @field_validator('Refund_Eligible')
    @classmethod
    def validate_refund_eligible(cls, v):
        """Validate refund eligibility is in allowed set"""
        if v not in VALID_REFUND_ELIGIBLE:
            raise ValueError(
                f"Invalid Refund_Eligible: '{v}'. Must be one of: {', '.join(sorted(VALID_REFUND_ELIGIBLE))}"
            )
        return v

    @field_validator('Is_Anomaly')
    @classmethod
    def validate_is_anomaly(cls, v):
        """Validate anomaly flag is in allowed set"""
        if v not in VALID_IS_ANOMALY:
            raise ValueError(
                f"Invalid Is_Anomaly: '{v}'. Must be one of: {', '.join(sorted(VALID_IS_ANOMALY))}"
            )
        return v
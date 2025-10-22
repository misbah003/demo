"""
INPUT VALIDATION MODULE FOR ML API
===================================

Provides Pydantic models and validators for VAT refund prediction API requests.
Ensures only valid categorical values are accepted and provides clear error messages.

Valid Categories (from trained model):
- Filing_Status: "On Time", "Late", "Very Late"
- Compliance_Flag: "Compliant", "Non-Compliant", "Under Review"
- Refund_Eligible: "Yes", "No"
- Is_Anomaly: "Yes", "No"
- Region: "East", "North", "South", "West"
- Category: "Retail", "Manufacturing", "Hospitality", "IT Services", "Pharmaceuticals", 
           "Healthcare", "Education", "FMCG", "Real Estate", "Others"
"""

from pydantic import BaseModel, Field, validator, ConstrainedList
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
    
    Validates all required fields and ensures categorical values are valid.
    """
    # Numeric fields with constraints
    Amount: float = Field(..., gt=0, description="Refund amount in EUR")
    VAT_Rate: float = Field(..., ge=0, le=100, description="VAT rate as percentage")
    Risk_Score: float = Field(..., ge=0, le=1, description="Risk score from 0 to 1")
    Annual_Turnover: float = Field(..., ge=0, description="Annual turnover in EUR")
    
    # Categorical fields with strict validation
    Category: str = Field(..., description="Product/Service category")
    Region: str = Field(..., description="Geographic region")
    Filing_Status: str = Field(..., description="Filing status")
    Compliance_Flag: str = Field(..., description="Compliance status")
    Refund_Eligible: str = Field(..., description="Refund eligibility")
    Is_Anomaly: str = Field(..., description="Anomaly flag")
    
    class Config:
        schema_extra = {
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
    
    @validator('Category')
    def validate_category(cls, v):
        """Validate category is in allowed set"""
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid Category: '{v}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
            )
        return v
    
    @validator('Region')
    def validate_region(cls, v):
        """Validate region is in allowed set"""
        if v not in VALID_REGIONS:
            raise ValueError(
                f"Invalid Region: '{v}'. Must be one of: {', '.join(sorted(VALID_REGIONS))}"
            )
        return v
    
    @validator('Filing_Status')
    def validate_filing_status(cls, v):
        """Validate filing status is in allowed set"""
        if v not in VALID_FILING_STATUS:
            raise ValueError(
                f"Invalid Filing_Status: '{v}'. Must be one of: {', '.join(sorted(VALID_FILING_STATUS))}"
            )
        return v
    
    @validator('Compliance_Flag')
    def validate_compliance_flag(cls, v):
        """Validate compliance flag is in allowed set"""
        if v not in VALID_COMPLIANCE_FLAG:
            raise ValueError(
                f"Invalid Compliance_Flag: '{v}'. Must be one of: {', '.join(sorted(VALID_COMPLIANCE_FLAG))}"
            )
        return v
    
    @validator('Refund_Eligible')
    def validate_refund_eligible(cls, v):
        """Validate refund eligibility is in allowed set"""
        if v not in VALID_REFUND_ELIGIBLE:
            raise ValueError(
                f"Invalid Refund_Eligible: '{v}'. Must be one of: {', '.join(sorted(VALID_REFUND_ELIGIBLE))}"
            )
        return v
    
    @validator('Is_Anomaly')
    def validate_is_anomaly(cls, v):
        """Validate anomaly flag is in allowed set"""
        if v not in VALID_IS_ANOMALY:
            raise ValueError(
                f"Invalid Is_Anomaly: '{v}'. Must be one of: {', '.join(sorted(VALID_IS_ANOMALY))}"
            )
        return v


class BatchPredictionRequest(BaseModel):
    """Schema for /batch-predict endpoint requests"""
    transactions: list = Field(..., description="List of prediction requests")
    
    class Config:
        schema_extra = {
            "example": {
                "transactions": [
                    {
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
                ]
            }
        }
    
    @validator('transactions')
    def validate_transactions(cls, v):
        """Validate each transaction in the batch"""
        if len(v) < 1:
            raise ValueError("transactions must contain at least 1 item")
        validated = []
        for i, transaction in enumerate(v):
            try:
                validated.append(PredictionRequest(**transaction))
            except ValueError as e:
                raise ValueError(f"Transaction {i}: {str(e)}")
        return validated


class ExplainRequest(BaseModel):
    """Schema for /explain endpoint requests"""
    Amount: float = Field(..., gt=0, description="Refund amount in EUR")
    VAT_Rate: float = Field(..., ge=0, le=100, description="VAT rate as percentage")
    Risk_Score: float = Field(..., ge=0, le=1, description="Risk score from 0 to 1")
    Annual_Turnover: float = Field(..., ge=0, description="Annual turnover in EUR")
    
    Category: str = Field(..., description="Product/Service category")
    Region: str = Field(..., description="Geographic region")
    Filing_Status: str = Field(..., description="Filing status")
    Compliance_Flag: str = Field(..., description="Compliance status")
    Refund_Eligible: str = Field(..., description="Refund eligibility")
    Is_Anomaly: str = Field(..., description="Anomaly flag")
    
    class Config:
        schema_extra = {
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
    
    @validator('Category')
    def validate_category(cls, v):
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid Category: '{v}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
            )
        return v
    
    @validator('Region')
    def validate_region(cls, v):
        if v not in VALID_REGIONS:
            raise ValueError(
                f"Invalid Region: '{v}'. Must be one of: {', '.join(sorted(VALID_REGIONS))}"
            )
        return v
    
    @validator('Filing_Status')
    def validate_filing_status(cls, v):
        if v not in VALID_FILING_STATUS:
            raise ValueError(
                f"Invalid Filing_Status: '{v}'. Must be one of: {', '.join(sorted(VALID_FILING_STATUS))}"
            )
        return v
    
    @validator('Compliance_Flag')
    def validate_compliance_flag(cls, v):
        if v not in VALID_COMPLIANCE_FLAG:
            raise ValueError(
                f"Invalid Compliance_Flag: '{v}'. Must be one of: {', '.join(sorted(VALID_COMPLIANCE_FLAG))}"
            )
        return v
    
    @validator('Refund_Eligible')
    def validate_refund_eligible(cls, v):
        if v not in VALID_REFUND_ELIGIBLE:
            raise ValueError(
                f"Invalid Refund_Eligible: '{v}'. Must be one of: {', '.join(sorted(VALID_REFUND_ELIGIBLE))}"
            )
        return v
    
    @validator('Is_Anomaly')
    def validate_is_anomaly(cls, v):
        if v not in VALID_IS_ANOMALY:
            raise ValueError(
                f"Invalid Is_Anomaly: '{v}'. Must be one of: {', '.join(sorted(VALID_IS_ANOMALY))}"
            )
        return v


class ComparisonRequest(BaseModel):
    """Schema for /compare-predictions endpoint requests"""
    predictions: list = Field(..., description="List of 2-5 prediction requests")
    
    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {
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
                ]
            }
        }
    
    @validator('predictions')
    def validate_predictions(cls, v):
        """Validate each prediction in the comparison"""
        if len(v) < 2 or len(v) > 5:
            raise ValueError("predictions must contain between 2 and 5 items")
        validated = []
        for i, prediction in enumerate(v):
            try:
                validated.append(PredictionRequest(**prediction))
            except ValueError as e:
                raise ValueError(f"Prediction {i}: {str(e)}")
        return validated


def validate_request(data: dict, model_class) -> tuple[bool, str, Optional[BaseModel]]:
    """
    Validate request data against schema.
    
    Returns:
        tuple: (is_valid, error_message, validated_data)
    """
    try:
        validated = model_class(**data)
        return True, "", validated
    except ValueError as e:
        error_msg = str(e)
        logger.warning(f"Validation error: {error_msg}")
        return False, error_msg, None


def get_validation_reference():
    """
    Returns a dictionary of valid values for API consumers.
    Useful for auto-complete, documentation, or client-side validation.
    """
    return {
        "Filing_Status": sorted(list(VALID_FILING_STATUS)),
        "Compliance_Flag": sorted(list(VALID_COMPLIANCE_FLAG)),
        "Refund_Eligible": sorted(list(VALID_REFUND_ELIGIBLE)),
        "Is_Anomaly": sorted(list(VALID_IS_ANOMALY)),
        "Region": sorted(list(VALID_REGIONS)),
        "Category": sorted(list(VALID_CATEGORIES))
    }
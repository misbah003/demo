from pydantic import BaseModel, Field, field_validator

class TestModel(BaseModel):
    Category: str = Field(..., description="Category")

    @field_validator('Category')
    @classmethod
    def validate_category(cls, v):
        if v not in ["A", "B"]:
            raise ValueError("Invalid")
        return v

# Test
try:
    t = TestModel(Category="A")
    print("Success")
except Exception as e:
    print(e)
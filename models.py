from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)

class Category(BaseModel):
    id: int
    title: str = Field(..., min_length=2, max_length=50)
class Record(BaseModel):
    id: int
    user_id: int = Field(..., ge=1)
    category_id: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
    timestamp: datetime

    @field_validator("timestamp")
    @classmethod
    def validate_date(cls, value: datetime) -> datetime:
        if value > datetime.now():
            raise ValueError("Timestamp cannot be in the future")
        return value
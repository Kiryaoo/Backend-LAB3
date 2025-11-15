from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str

class Category(BaseModel):
    id: int
    title: str

class Record(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: float
    timestamp: datetime
from pydantic import BaseModel,Field
from typing import Literal



class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
    
class UserLogin(BaseModel):
    email: str
    password: str 
    
class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    type: Literal["income", "expense"] 
    category: str =Field(min_length=1)
    description: str | None = None



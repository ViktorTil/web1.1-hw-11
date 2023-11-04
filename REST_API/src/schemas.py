from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime

class ContactModel(BaseModel):
    first_name : str = Field(min_length=3)
    last_name : str = Field(min_length=3)
    email : EmailStr
    phone : str = Field(min_length=10, max_length=20)
    #email: str = Field(default = "example@com.ua", regex ="")
    birthday : date
    
class ContactResponse(BaseModel):
    id: int = 1
    first_name : str
    last_name : str
    email: EmailStr
    phone : str
    birthday : date
    create_at: datetime
    update_at: datetime
    
    class Config:
        orm_mode = True
 
    



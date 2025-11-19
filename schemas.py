from pydantic import BaseModel, ConfigDict
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    
    model_config = ConfigDict(
        from_attributes=True,  # Changed from orm_mode
        json_schema_extra={
            "example": {
                "username": "XXXXXXX",
                "email": "johndoe@example.com",
                "password": "XXXXXXXXXXX",
                "is_active": True,
                "is_staff": False
            }
        }
    )
        
class Settings(BaseModel):
    authjwt_secret_key: str = '9db6d854eb823897d6404bff365b17d424818a7a7209a46e07f7d6c7a7351b62' 
    
class LoginModel(BaseModel):
    username: str
    password: str
    
class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int 
    pizza_size: Optional[str] = "SMALL"  
    order_status: Optional[str] = "PENDING"  
    user_id: Optional[int] = None  

    model_config = ConfigDict(
        from_attributes=True,  # Changed from orm_mode
        json_schema_extra={  
            "example": {
                "quantity": 2,
                "pizza_size": "SMALL"
            }
        }
    )
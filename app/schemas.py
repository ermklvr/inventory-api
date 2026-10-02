from pydantic import BaseModel, ConfigDict, Field

from decimal import Decimal

from .models import MovementType

from datetime import datetime


class ProductCreate(BaseModel):
    model_config = ConfigDict(
        extra = 'forbid',
        str_strip_whitespace=True
    )
    
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0, max_digits=10,decimal_places=2)
    stock_quantity: int = Field(ge=0)
    category_id: int = Field(gt=0)
    
    
class ProductResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
        )
    
    id: int
    name: str
    price: Decimal
    stock_quantity: int
    category_id: int

class CategoryCreate(BaseModel):
    model_config = ConfigDict(
            extra = 'forbid',
            str_strip_whitespace=True
        )
    
    name: str = Field(min_length=1)
    
class CategoryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )    
    id: int
    name: str 
    
class MovementCreate(BaseModel):
    model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
)
    product_id: int = Field(gt=0)
    type: MovementType
    quantity: int = Field(gt=0)
    


class MovementResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    ) 
    id: int
    product_id: int
    type: MovementType
    quantity: int
    date: datetime
      
class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category_id: int = Field(gt=0)
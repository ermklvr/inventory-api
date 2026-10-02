from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product,Category
from ..schemas import ProductCreate, ProductResponse, ProductUpdate

from ..exceptions import ProductNotFoundError, CategoryNotFoundError

from .. import crud


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

#CRUD

#CREATE
@router.post("/", response_model=ProductResponse)
def new_product (
   product: ProductCreate,
   db: Session = Depends(get_db)
):
    try:
        return crud.new_product(db,product)
        
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
    
   

#READ
@router.get("/" , response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@router.get("/{product_id}",  response_model=ProductResponse)
def get_product_by_id (
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud.get_product_by_id(db,product_id)
    
    if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

#UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_product(db,product_id,product)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    except CategoryNotFoundError:
            raise HTTPException(status_code=404, detail="Category not found")

#DELETE
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)                            
):
    try:
        crud.delete_product(db,product_id)
   
    except ProductNotFoundError:
       raise HTTPException(status_code = 404, detail="Product not found")
    return 
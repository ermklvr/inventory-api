from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product,Category,Movement, MovementType
from ..schemas import MovementCreate, MovementResponse
from ..exceptions import *

from decimal import Decimal

from .. import crud

router = APIRouter(
    prefix="/movements",
    tags=["Movements"]
)


#CRUD

#CREATE

@router.post("/", response_model=MovementResponse)
def create_movement(
    movement:MovementCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_movement(db, movement)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="Product not found")
        
    except InsufficientStockError:
        raise HTTPException(
            status_code=409, 
            detail="Insufficient stock")
    except ProductInactiveError: 
        raise HTTPException( 
            status_code=409,
            detail="Product is inactive")
        
    
#READ
@router.get("/" , response_model=list[MovementResponse])
def get_movements(db: Session = Depends(get_db)):
    return crud.get_movements(db)

@router.get("/{movement_id}",  response_model=MovementResponse)
def get_movement_by_id(
    movement_id: int,
    db: Session = Depends(get_db)
):
    movement = crud.get_movement_by_id(db,movement_id)

    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement

#DELETE
@router.delete("/{movement_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db)
):
    try:
        crud.delete_movement(db,movement_id)    
    except MovementNotFoundError:
        raise HTTPException(status_code=404,
                            detail="Movement not found")
    except InsufficientStockError:
        raise HTTPException(status_code=409,
        detail="Cannot delete: stock would become negative")
    except ProductNotFoundError:
        raise HTTPException(status_code = 404, 
                            detail="Product not found") 
    return


from .models import Category, Product, Movement, MovementType

from .exceptions import *






#------------REGRA DE ESTOQUE-------------
def update_stock(movement,product,reverse=False):
    quantity = movement.quantity
    
    if movement.type == MovementType.IN:
        quantity = -quantity if reverse else quantity
    
    elif movement.type == MovementType.OUT:
        quantity = quantity if reverse else -quantity
        
    if product.stock_quantity + quantity < 0:
        raise InsufficientStockError()
    
    product.stock_quantity += quantity
      
#-----------CRUD--------------

#-----------CATEGORY-----------
#-----------CREATE ------------
def create_category(db,category):
    new_category = Category(name=category.name)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
        
    return new_category

#-----------READ------------
#----Lê todos os ID
def get_categories(db):
    return db.query(Category).order_by(Category.id.asc()).all()

#---Lê somente um ID
def get_category_by_id(db,category_id):
    return db.query(Category).filter(Category.id == category_id).first()

#-----------UPDATE------------
def update_category(db, category_id,category):
    up_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not up_category:
        raise CategoryNotFoundError()
    
    up_category.name  = category.name
    db.commit()
    db.refresh(up_category)
    return up_category
    
    

#-----------DELETE------------
def delete_category(db,category_id):
    del_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not del_category:
        raise CategoryNotFoundError()
    
    if del_category.products:         
        raise CategoryHasProductsError()
    
    db.delete(del_category)
    db.commit()
    
    return del_category





#-----------PRODUCTS-----------
#-----------CREATE ------------
def new_product(db, product):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    
    if not category:
        raise CategoryNotFoundError()
    
    created_product = Product(
        name = product.name,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id 
        )
    
    db.add(created_product)
    db.commit()
    db.refresh(created_product)
        
    return created_product
#-----------READ------------
#---- todos os produtos
def get_products(db):
    return db.query(Product).filter(Product.active.is_(True)).order_by(Product.id.asc()).all()

#--- um unico produto
def get_product_by_id(db,product_id):
    return db.query(Product).filter(Product.id == product_id, Product.active.is_(True)).first()
#-----------UPDATE------------
def update_product(db, product_id, product): 
    up_product = db.query(Product).filter(Product.id == product_id).first()

    if not up_product:
        raise ProductNotFoundError()

    category = db.query(Category).filter(Category.id == product.category_id).first()

    if not category:
        raise CategoryNotFoundError()

    up_product.name = product.name
    up_product.price = product.price
    up_product.category_id = product.category_id
    db.commit()
    db.refresh(up_product)
    return up_product
   
#-----------DELETE------------
def delete_product(db,product_id):
    deleted_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not deleted_product:
        raise ProductNotFoundError()
    
    deleted_product.active = False
    db.commit()
        
    return deleted_product





#-----------MOVEMENTS-----------
#-----------CREATE ------------
def create_movement(db, movement):
    try:
        product = (db.query(Product).with_for_update().filter(Product.id == movement.product_id).first())

        if not product:
            raise ProductNotFoundError()

        if not product.active:
            raise ProductInactiveError()

        update_stock(movement, product)

        new_movement = Movement(
            product_id=movement.product_id,
            type=movement.type,
            quantity=movement.quantity
        )

        db.add(new_movement)
        db.commit()
        db.refresh(new_movement)

        return new_movement

    except Exception:
        db.rollback()
        raise
        

#-----------READ ------------
def get_movements(db):
    return db.query(Movement).order_by(Movement.id.asc()).all()

def get_movement_by_id(db,movement_id):
    return db.query(Movement).filter(Movement.id == movement_id).first()
#-----------DELETE ------------
def delete_movement(db,movement_id):
    try:
        deleted_movement = db.query(Movement).filter(Movement.id == movement_id).first()
        
        if not deleted_movement:
                raise MovementNotFoundError()
        
        product = db.query(Product).with_for_update().filter(Product.id == deleted_movement.product_id).first()
            
        if not product:
            raise ProductNotFoundError()
    
        update_stock(deleted_movement,product, reverse=True)  
            
        db.delete(deleted_movement)
        db.commit()
                
        return deleted_movement
    except Exception:
        db.rollback()
        raise

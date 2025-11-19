from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
import jwt
from database import get_db
from models import User, Order
from schemas import OrderModel
from pydantic import BaseModel

class OrderStatusUpdate(BaseModel):
    order_status: str
from fastapi.encoders import jsonable_encoder
from auth_routes import SECRET_KEY, ALGORITHM


# Create the router
order_router = APIRouter(prefix='/order', tags=['order'])

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_staff_user(current_user: str, db: Session):
    """Helper function to get and validate staff user"""
    user = db.query(User).filter(User.username == current_user).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a staff member"
        )
    
    return user

# Define a simple hello endpoint
@order_router.get("/hello")
def hello(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}"}

@order_router.post("/", status_code=status.HTTP_201_CREATED)
def place_an_order(
    order: OrderModel, 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
        user_id=user.id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)



@order_router.get("/orders")
def list_all_orders(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_staff_user(current_user, db)
    orders = db.query(Order).all()
    return jsonable_encoder(orders)


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_order_by_id(
    id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_staff_user(current_user, db)
    
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return jsonable_encoder(order)

@order_router.put('/{id}')
def update_order(
    id: int,
    order: OrderModel,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_staff_user(current_user, db)
    
    existing_order = db.query(Order).filter(Order.id == id).first()
    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    existing_order.pizza_size = order.pizza_size
    existing_order.quantity = order.quantity
    
    db.commit()
    db.refresh(existing_order)
    
    return jsonable_encoder(existing_order)

@order_router.delete('/{id}')
def delete_order(
    id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_staff_user(current_user, db)
    
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    db.delete(order)
    db.commit()
    
    return {"message": "Order deleted successfully"}

@order_router.patch('/{id}/status')
def update_order_status(
    id: int,
    status_update: OrderStatusUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_staff_user(current_user, db)
    
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.order_status = status_update.order_status
    db.commit()
    db.refresh(order)
    
    return jsonable_encoder(order)

@order_router.get('/user/orders')
def get_user_orders(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return jsonable_encoder(user.orders) 

@order_router.get('/user/orders/{id}')
def get_specific_order(
    id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    order = db.query(Order).filter(
        Order.id == id,
        Order.user_id == user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return jsonable_encoder(order)
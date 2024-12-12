from sqlalchemy.orm import Session
from database import db
from models.order import Order
from models.product import Product
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(order):
    return None


# Save New Order Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(order_data):
    try:
        if order_data['customerId'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                product = session.get(Product, order_data['productId'])
                if not product:
                    raise ValueError("Invalid product ID")
                
                total_price = round((order_data['quantity'] * product.price), 2)
                new_order = Order(customerId=order_data['customerId'], productId=order_data['productId'], quantity=order_data['quantity'], totalPrice = total_price)
                session.add(new_order)
                session.commit()
            session.refresh(new_order)
            return new_order
        
    except Exception as e:
        raise e
    

# Get All Orders
def find_orders():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders


# Paginate Orders
def paginate_orders(page=1, per_page=10):
    query = db.session.query(Order).order_by(Order.createdAt.desc())
    orders = query.offset((page - 1) * per_page).limit(per_page).all()
    total_items = db.session.query(Product).count()

    return {
        'orders': orders,
        'totalItems': total_items,
    }
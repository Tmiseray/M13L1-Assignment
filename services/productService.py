from sqlalchemy.orm import Session
from database import db
from models.product import Product
from models.order import Order
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(product):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(product_data):
    try:
        if product_data['name'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_product = Product(name=product_data['name'], price=product_data['price'], createdBy=product_data['createdBy'])
                session.add(new_product)
                session.commit()
            session.refresh(new_product)
            return new_product
        
    except Exception as e:
        raise e
    

def find_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products

def top_selling_products():
    query = select(
        Product.name.label('productName'),
        func.sum(Order.quantity).label('totalItemsSold')
    ).join(Order, Product.id == Order.productId)
    query = query.group_by(Product.name).order_by(Order.quantity, 'DESC')

    products = db.session.execute(query).all()
    return products
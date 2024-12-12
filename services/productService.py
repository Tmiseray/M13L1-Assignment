from sqlalchemy.orm import Session
from database import db
from models.product import Product
from models.order import Order
from circuitbreaker import circuit
from sqlalchemy import select, func, desc


def fallback_function(product):
    return None


# Save New Product Data
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
    

# Get All Products
def find_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products


# Paginate Products
def paginate_products(page=1, per_page=10):
    query = db.session.query(Product).order_by(Product.name.desc())
    products = query.offset((page - 1) * per_page).limit(per_page).all()
    total_items = db.session.query(Product).count()

    return {
        'products': products,
        'totalItems': total_items,
    }


# Top Selling Products
def top_selling_products():
    query = (
        select(
            Product.name.label('productName'),
            func.sum(Order.quantity).label('totalItemsSold')
        )
        .join(Order, Product.id == Order.productId)
        .group_by('productName')
        .order_by(desc('totalItemsSold'))
    )

    products = db.session.execute(query).all()
    return products
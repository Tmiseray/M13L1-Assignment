from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from models.order import Order
from circuitbreaker import circuit
from sqlalchemy import select, func


def fallback_function(customer):
    return None


@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_data):
    try:
        if customer_data['name'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
                session.add(new_customer)
                session.commit()
            session.refresh(new_customer)
            return new_customer
        
    except Exception as e:
        raise e
    

def find_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers


def customers_loyalty_value():
    query = (
        select(
            Customer.name.label('customerName'),
            func.sum(Order.totalPrice).label('lifetimeLoyaltyValue')
        )
        .join(Order, Customer.id == Order.customerId)
        .group_by(Customer.name)
        .having(func.sum(Order.totalPrice) >= 50)
    )

    loyal_customers = db.session.execute(query).all()
    return loyal_customers
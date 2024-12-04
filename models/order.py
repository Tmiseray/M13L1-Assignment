from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import event
from models.product import Product

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('Products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(db.Float, nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates='orders')
    product: Mapped['Product'] = db.relationship(primaryjoin='Order.product_id == Product.id')
    

@event.listens_for(Order, 'before_update')
def update_total_price(mapper, connection, target):
    if target.product_id:
        product = db.session.get(Product, target.product_id)
        if product:
            target.total_price = target.quantity * product.price
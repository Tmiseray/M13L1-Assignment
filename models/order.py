from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('Products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(db.Float, nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates='orders')
    product: Mapped['Product'] = db.relationship(primaryjoin='Order.product_id == Product.id')
    
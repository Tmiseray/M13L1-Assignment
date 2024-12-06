from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Production(Base):
    __tablename__ = 'Production'
    id: Mapped[int] = mapped_column(primary_key=True)
    productId: Mapped[int] = mapped_column(db.ForeignKey('Products.id'), nullable=False)
    quantityProduced: Mapped[int] = mapped_column(db.Integer, nullable=False)
    dateProduced: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    createdAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now())
    updatedAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    product: Mapped['Product'] = db.relationship(primaryjoin='Production.productId == Product.id')
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import event, select
import datetime

class Production(Base):
    __tablename__ = 'Production'
    id: Mapped[int] = mapped_column(primary_key=True)
    productId: Mapped[int] = mapped_column(db.ForeignKey('Products.id'), nullable=False)
    quantityProduced: Mapped[int] = mapped_column(db.Integer, nullable=False)
    dateProduced: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    createdBy: Mapped[int] = mapped_column(db.ForeignKey('Employees.id'), nullable=False)
    createdAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now())
    updatedBy: Mapped[int] = mapped_column(db.ForeignKey('Employees.id'), nullable=True)
    updatedAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    product: Mapped['Product'] = db.relationship(primaryjoin='Production.productId == Product.id')
    creator: Mapped['Employee'] = db.relationship(primaryjoin='Production.createdBy == Employee.id')
    updater: Mapped['Employee'] = db.relationship(primaryjoin='Production.updatedBy == Employee.id')

@event.listens_for(Production, 'before_insert')
def before_insert(mapper, connection, target):
    if not target.createdBy:
        raise ValueError("Missing required field during creation: 'createdBy'.")
    
    if not target.updatedBy:
        target.updatedBy = target.createdBy

@event.listens_for(Production, 'before_update')
def before_update(mapper, connection, target):
    if target.createdBy:
        original = connection.execute(
            select([Production.createdBy]).where(Production.id == target.id)
        ).fetchone()
        if original and original[0] != target.createdBy:
            raise ValueError("Field cannot be changed after creation: 'createdBy'.")
        
    if not target.updatedBy:
        raise ValueError("Missing required field during update: 'updatedBy'.")
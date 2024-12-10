from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    createdBy: Mapped[int] = mapped_column(db.ForeignKey('Employees.id'), nullable=False)
    createdAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now())
    updatedBy: Mapped[int] = mapped_column(db.ForeignKey('Employees.id'), nullable=True)
    updatedAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    creator: Mapped['Employee'] = db.relationship(primaryjoin='Product.createdBy == Employee.id')
    updater: Mapped['Employee'] = db.relationship(primaryjoin='Product.updatedBy == Employee.id')
from sqlalchemy.orm import Mapped, mapped_column
from models.employee import Employee
from models.customer import Customer
from database import db, Base
from sqlalchemy import and_
import datetime

class User(Base):
    __tablename__= 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[str] = mapped_column(db.String(20), nullable=False)
    accountId: Mapped[int] = mapped_column(db.Integer, nullable=False)

    createdAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now())
    updatedAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    employee: Mapped['Employee'] = db.relationship(
        'Employee',
        primaryjoin=and_(
            accountId == Employee.id,
            role == "admin"
            ),
        foreign_keys=[accountId],
        uselist=False,
        )

    customer: Mapped['Customer'] = db.relationship(
        'Customer',
        primaryjoin=and_(
            accountId == Customer.id,
            role == "user"
            ),
        foreign_keys=[accountId],
        uselist=False,
        )
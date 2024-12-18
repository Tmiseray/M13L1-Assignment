from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
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

    employee: Mapped['Employee'] = db.relationship(uselist=False, primary_join='and_(User.accountId == Employee.id, User.role == "admin")')

    customer: Mapped['Customer'] = db.relationship(uselist=False, primary_join='and_(User.accountId == Customer.id, User.role == "user")')
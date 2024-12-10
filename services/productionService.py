from sqlalchemy.orm import Session
from database import db
from models.production import Production
from models.employee import Employee
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(production):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(production_data):
    try:
        if production_data['productId'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_production = Production(productId=production_data['productId'], quantityProduced=production_data['quantityProduced'], dateProduced=production_data['dateProduced'])
                session.add(new_production)
                session.commit()
            session.refresh(new_production)
            return new_production
        
    except Exception as e:
        raise e
    

def find_productions():
    query = select(Production)
    productions = db.session.execute(query).scalars().all()
    return productions

def employees_total_productions():
    query = select(
        Employee.name.label('employeeName'),
        func.sum(Production.quantityProduced).label('totalItemsProduced')
        .join(Production).where(Employee.id == Production.updatedBy)
        .group_by(Employee.name)
        )
    productions = db.session.execute(query).all()
    return productions
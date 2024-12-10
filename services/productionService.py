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
                if not production_data.get('createdBy'):
                    raise ValueError("Missing required field: 'createdBy'")
                
                new_production = Production(productId=production_data['productId'],
                        quantityProduced=production_data['quantityProduced'],
                        dateProduced=production_data['dateProduced'],
                        createdBy=production_data['createdBy']
                    )
                
                if not production_data.get('updatedBy'):
                    new_production.updatedBy = production_data['createdBy']
                    
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
        func.sum(Production.quantityProduced).label('totalItemsProduced')).join(Production, Employee.id == Production.updatedBy)
    query = query.group_by(Employee.name)
        
    productions = db.session.execute(query).all()
    return productions
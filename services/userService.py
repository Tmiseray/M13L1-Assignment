from sqlalchemy.orm import Session
from database import db
from models.employee import Employee
from models.user import User
from circuitbreaker import circuit
from sqlalchemy import select, func
from utils.util import encode_token


def fallback_function(user):
    return None


# User Login
def login(username, password):
    user = (db.session.execute(db.select(User).where(User.username == username, User.password == password)).scalar_one_or_none())
    roleName = user.role
    if user:
        auth_token = encode_token(user.id, roleName)
        resp = {
            "status": "success",
            "message": "Successfully logged in",
            "authToken": auth_token
        }
        return resp
    else:
        return None
    

# Save New User Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(user_data):
    try:
        if user_data['username'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_user = User(username=user_data['username'],
                                password=user_data['password'],
                                role=user_data['role'],
                                accountId=user_data['accountId'])
                session.add(new_user)
                session.commit()
            session.refresh(new_user)
            return new_user
        
    except Exception as e:
        raise e
    

# Get All Users
def find_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users

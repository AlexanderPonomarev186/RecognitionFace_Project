from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import uuid


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:CasperTo360Flip@localhost:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)

def create_user(datab: get_db()):
    for db in datab:
        db_user = User(id=uuid.uuid4())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_user(datab: get_db(), user_id: uuid.UUID):
    for db in datab: return db.query(User).filter(User.id == user_id).first()


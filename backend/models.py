from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class Listings(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    location = Column(String)
    salary = Column(String)
    company = Column(Integer, ForeignKey("companies.id"))

class Companies(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    contactEmail = Column(String)
    contactPhone = Column(String)
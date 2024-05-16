from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class CompanyBase(BaseModel):
   name: str
   description:str
   contactEmail: EmailStr
   contactPhone: str

class JobListingBase(BaseModel):
    title: str
    type: str
    description: str
    location: str
    salary: str
    company: int

class JobListingCreate(JobListingBase):
    pass

class JobListing(JobListingBase):
    id: int

    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/add-job")
async def add_job(job: JobListingCreate, db: db_dependency):
    db_job = models.Listings(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.post("/add-company")
async def add_company(company: CompanyCreate,db: db_dependency):
    db_company = models.Companies(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr
from typing import Annotated, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class JobListingBase(BaseModel):
    title: str
    type: str
    description: str
    location: str
    salary: str
    companyName: str
    companyDescription:str
    contactEmail: EmailStr
    contactPhone: str
class JobListingModel(JobListingBase):
    id: int

    class Config:
        from_attributes=True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/add-job", response_model=JobListingModel)
async def add_job(job: JobListingBase, db: db_dependency):
    db_job = models.Listings(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.get("/jobs", response_model=List[JobListingModel])
async def get_jobs(db: db_dependency,limit: int = Query(None)):
    query = db.query(models.Listings)
    if limit:
        query = query.limit(limit)
    jobs = query.all()
    return jobs

@app.get("/jobs/{id}")
async def get_job(id: str ,db: db_dependency):
    job = db.query(models.Listings).filter(models.Listings.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job Listing not found")
    return job

@app.put("/jobs/{id}", response_model=JobListingModel)
async def update_job(id: str, updatedJob: JobListingBase, db: db_dependency):
    job = db.query(models.Listings).filter(models.Listings.id == id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job Listing not found")

    for key, value in updatedJob.dict().items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job

@app.delete("/jobs/{id}")
async def delete_job(id:str, db: db_dependency):
    job = db.query(models.Listings).filter(models.Listings.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job Listing not found")
    db.delete(job)
    db.commit()
    return job
    
  

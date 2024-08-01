# api.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Employee, JobPost
from vectorize import vectorize_employee, vectorize_job_post
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class LoginRequest(BaseModel):
    employee_name: str
    password: str

class EmployeeData(BaseModel):
    employee_info: dict
    grades: List[dict]
    skills: List[dict]
    spi: Optional[dict]
    evaluations: List[dict]
    departments: List[dict]

class JobRecommendation(BaseModel):
    job_id: int
    job_title: str
    details: str

@app.post("/login", response_model=EmployeeData)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == request.employee_name).first()
    if employee is None or employee.password != request.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    employee_data = get_all_employee_data(db, employee)
    return employee_data

@app.get("/job_recommendations", response_model=List[JobRecommendation])
def job_recommendations(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_data = get_all_employee_data(db, employee)
    employee_vector = vectorize_employee(employee_data)
    job_posts = db.query(JobPost).all()
    job_vectors = {job.job_post_id: vectorize_job_post(job) for job in job_posts}
    recommendations = get_job_recommendations(employee_data, employee_vector, job_posts, job_vectors)
    return recommendations

"""
FastAPI Registration Service
Handles student registration, registration verification, and registration reports.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import httpx
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WEMS Registration Service",
    description="Student registration and registration management service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000")
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "your-service-token-here")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/wems")

# Security
security = HTTPBearer()

# Pydantic Models
class StudentBase(BaseModel):
    name: str
    name_bangla: Optional[str] = None
    father_name: str
    mother_name: str
    date_of_birth: str
    gender: str
    nationality: str = "Bangladeshi"
    religion: str
    present_address: str
    permanent_address: str
    phone: str
    email: Optional[EmailStr] = None
    blood_group: Optional[str] = None

class StudentCreate(StudentBase):
    madrasha_id: int
    marhala_id: int
    class_id: Optional[int] = None
    roll_number: Optional[str] = None
    registration_number: Optional[str] = None
    previous_institution: Optional[str] = None
    transfer_certificate_number: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    name_bangla: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    present_address: Optional[str] = None
    permanent_address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    blood_group: Optional[str] = None
    class_id: Optional[int] = None
    roll_number: Optional[str] = None

class Student(StudentBase):
    id: int
    madrasha_id: int
    marhala_id: int
    class_id: Optional[int] = None
    roll_number: Optional[str] = None
    registration_number: Optional[str] = None
    previous_institution: Optional[str] = None
    transfer_certificate_number: Optional[str] = None
    registration_status: str
    registration_date: datetime
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OldStudentBase(BaseModel):
    old_registration_number: str
    old_madrasha_name: str
    old_madrasha_code: str
    exam_year: int
    passing_year: int
    result: str
    gpa: Optional[float] = None
    board: str

class OldStudentCreate(OldStudentBase):
    student_id: int
    marhala_id: int
    verification_status: str = "pending"

class OldStudent(OldStudentBase):
    id: int
    student_id: int
    marhala_id: int
    verification_status: str
    verified_by: Optional[int] = None
    verification_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RegistrationOverview(BaseModel):
    total_students: int
    active_registrations: int
    pending_registrations: int
    verified_registrations: int
    rejected_registrations: int
    registrations_by_marhala: dict
    registrations_by_madrasha: dict
    monthly_registrations: dict

class UserInfo(BaseModel):
    id: int
    email: str
    user_type: str
    permissions: List[str]

# Authentication Dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT token with auth service and get current user"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/auth/validate/",
                json={
                    "token": credentials.credentials,
                    "service_name": "registration-service"
                },
                headers={"X-Service-Token": SERVICE_TOKEN}
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )

            data = response.json()
            if not data.get('valid'):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token validation failed"
                )

            return UserInfo(**data['user'])

    except httpx.RequestError as e:
        logger.error(f"Auth service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )

# Permission Check
async def require_permission(permission: str, current_user: UserInfo = Depends(get_current_user)):
    """Require specific permission"""
    if permission not in current_user.permissions and 'admin' not in current_user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission '{permission}' required"
        )
    return current_user

# Database Connection (Simplified for demo)
class Database:
    """Simple database connection manager"""
    def __init__(self):
        self.db_url = DATABASE_URL

    async def execute_query(self, query: str, params: dict = None):
        """Execute database query (placeholder)"""
        logger.info(f"Executing query: {query}")
        logger.info(f"Parameters: {params}")
        return []

db = Database()

# API Routes

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "registration-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/registration/overview", response_model=RegistrationOverview)
async def get_registration_overview(
    current_user: UserInfo = Depends(get_current_user)
):
    """Get registration overview statistics"""
    try:
        # Generate registration overview
        return RegistrationOverview(
            total_students=5000,
            active_registrations=4500,
            pending_registrations=200,
            verified_registrations=4200,
            rejected_registrations=100,
            registrations_by_marhala={
                "Dakhil": 2000,
                "Alim": 1500,
                "Fazil": 1000,
                "Kamil": 500
            },
            registrations_by_madrasha={
                "Dhaka": 1500,
                "Chittagong": 1200,
                "Rajshahi": 1000,
                "Khulna": 800,
                "Sylhet": 500
            },
            monthly_registrations={
                "Jan": 200,
                "Feb": 180,
                "Mar": 220,
                "Apr": 190,
                "May": 210,
                "Jun": 200
            }
        )

    except Exception as e:
        logger.error(f"Error generating registration overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate registration overview"
        )

@app.get("/api/registration/students/", response_model=List[Student])
async def get_students(
    skip: int = 0,
    limit: int = 20,
    madrasha_id: Optional[int] = None,
    marhala_id: Optional[int] = None,
    registration_status: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of registered students"""
    try:
        # Database query would go here
        # For demo, return empty list
        return []

    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch students"
        )

@app.post("/api/registration/students/", response_model=Student)
async def create_student_registration(
    student: StudentCreate,
    current_user: UserInfo = Depends(require_permission("registration_create"))
):
    """Create new student registration"""
    try:
        # Validate user permissions
        if 'madrasha_operations' not in current_user.permissions:
            # Check if user belongs to the specified madrasha
            # This would involve checking user's assigned madrasha
            pass

        # Generate registration number
        registration_number = f"REG{datetime.now().year}{datetime.now().month:02d}{datetime.now().day:02d}{student.madrasha_id:04d}"

        # Insert student into database
        query = """
        INSERT INTO students (name, name_bangla, father_name, mother_name, date_of_birth,
                             gender, nationality, religion, present_address, permanent_address,
                             phone, email, blood_group, madrasha_id, marhala_id, class_id,
                             roll_number, registration_number, previous_institution,
                             transfer_certificate_number, registration_status, registration_date,
                             created_by)
        VALUES (%(name)s, %(name_bangla)s, %(father_name)s, %(mother_name)s, %(date_of_birth)s,
                %(gender)s, %(nationality)s, %(religion)s, %(present_address)s, %(permanent_address)s,
                %(phone)s, %(email)s, %(blood_group)s, %(madrasha_id)s, %(marhala_id)s, %(class_id)s,
                %(roll_number)s, %(registration_number)s, %(previous_institution)s,
                %(transfer_certificate_number)s, 'pending', CURRENT_DATE, %(created_by)s)
        RETURNING id, created_at, updated_at, registration_date
        """

        params = {
            "name": student.name,
            "name_bangla": student.name_bangla,
            "father_name": student.father_name,
            "mother_name": student.mother_name,
            "date_of_birth": student.date_of_birth,
            "gender": student.gender,
            "nationality": student.nationality,
            "religion": student.religion,
            "present_address": student.present_address,
            "permanent_address": student.permanent_address,
            "phone": student.phone,
            "email": student.email,
            "blood_group": student.blood_group,
            "madrasha_id": student.madrasha_id,
            "marhala_id": student.marhala_id,
            "class_id": student.class_id,
            "roll_number": student.roll_number,
            "registration_number": registration_number,
            "previous_institution": student.previous_institution,
            "transfer_certificate_number": student.transfer_certificate_number,
            "created_by": current_user.id
        }

        # Execute database query
        result = await db.execute_query(query, params)

        # Return created student (mock response)
        return Student(
            id=1,
            **student.dict(),
            registration_number=registration_number,
            registration_status="pending",
            registration_date=datetime.now(),
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating student registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create student registration"
        )

@app.get("/api/registration/students/{student_id}", response_model=Student)
async def get_student(
    student_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get specific student by ID"""
    try:
        # Database query would go here
        # For demo, raise not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching student {student_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch student"
        )

@app.put("/api/registration/students/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    current_user: UserInfo = Depends(require_permission("registration_update"))
):
    """Update student information"""
    try:
        # Update student in database
        # For demo, return success response
        return Student(
            id=student_id,
            name=student.name or "John Doe",
            name_bangla=student.name_bangla,
            father_name=student.father_name or "Father Name",
            mother_name=student.mother_name or "Mother Name",
            date_of_birth=student.date_of_birth or "2000-01-01",
            gender=student.gender or "Male",
            nationality="Bangladeshi",
            religion=student.religion or "Islam",
            present_address=student.present_address or "Address",
            permanent_address=student.permanent_address or "Address",
            phone=student.phone or "01700000000",
            email=student.email,
            blood_group=student.blood_group,
            madrasha_id=1,
            marhala_id=1,
            class_id=student.class_id,
            roll_number=student.roll_number,
            registration_number="REG20240001",
            previous_institution="Previous School",
            transfer_certificate_number="TC123456",
            registration_status="updated",
            registration_date=datetime.now(),
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error updating student {student_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update student"
        )

@app.get("/api/registration/old-students/", response_model=List[OldStudent])
async def get_old_students(
    skip: int = 0,
    limit: int = 20,
    marhala_id: Optional[int] = None,
    verification_status: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of old student verifications"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching old students: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch old students"
        )

@app.post("/api/registration/old-students/", response_model=OldStudent)
async def create_old_student_verification(
    old_student: OldStudentCreate,
    current_user: UserInfo = Depends(require_permission("registration_create"))
):
    """Create old student verification record"""
    try:
        # Insert old student verification into database
        return OldStudent(
            id=1,
            **old_student.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating old student verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create old student verification"
        )

@app.post("/api/registration/old-students/{old_student_id}/verify")
async def verify_old_student(
    old_student_id: int,
    verification_status: str,
    remarks: Optional[str] = None,
    current_user: UserInfo = Depends(require_permission("registration_verify"))
):
    """Verify old student record"""
    try:
        # Update verification status in database
        return {
            "message": "Old student verification updated successfully",
            "old_student_id": old_student_id,
            "verification_status": verification_status,
            "verified_by": current_user.id,
            "verification_date": datetime.now(),
            "remarks": remarks
        }

    except Exception as e:
        logger.error(f"Error verifying old student {old_student_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify old student"
        )

@app.get("/api/registration/reports/student-list")
async def get_student_list_report(
    madrasha_id: Optional[int] = None,
    marhala_id: Optional[int] = None,
    registration_status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Generate student list report"""
    try:
        # Generate student list report
        return {
            "students": [],
            "summary": {
                "total_students": 0,
                "by_status": {},
                "by_marhala": {},
                "by_madrasha": {}
            },
            "filters": {
                "madrasha_id": madrasha_id,
                "marhala_id": marhala_id,
                "registration_status": registration_status,
                "start_date": start_date,
                "end_date": end_date
            }
        }

    except Exception as e:
        logger.error(f"Error generating student list report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate student list report"
        )

@app.get("/api/registration/reports/registration-statistics")
async def get_registration_statistics(
    year: Optional[int] = None,
    madrasha_id: Optional[int] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get registration statistics report"""
    try:
        # Generate registration statistics
        return {
            "year": year or datetime.now().year,
            "total_registrations": 0,
            "monthly_breakdown": {},
            "marhala_breakdown": {},
            "madrasha_breakdown": {},
            "status_breakdown": {
                "pending": 0,
                "verified": 0,
                "rejected": 0
            }
        }

    except Exception as e:
        logger.error(f"Error generating registration statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate registration statistics"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
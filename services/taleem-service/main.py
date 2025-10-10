"""
FastAPI Taleem Tarbiyat Service
Handles educational curriculum, student progress, teacher assignments, and class scheduling.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import httpx
import os
from datetime import datetime
import logging
import asyncpg

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WEMS Taleem Tarbiyat Service",
    description="Educational curriculum and student progress management service",
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/wems")

# Security
security = HTTPBearer()

# Pydantic Models
class SubjectBase(BaseModel):
    name: str
    name_bangla: str
    code: str
    description: Optional[str] = None
    marhala_id: int
    class_type: str  # theory, practical, both
    credit_hours: int
    passing_marks: int
    total_marks: int

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    name_bangla: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    class_type: Optional[str] = None
    credit_hours: Optional[int] = None
    passing_marks: Optional[int] = None
    total_marks: Optional[int] = None

class Subject(SubjectBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ClassScheduleBase(BaseModel):
    class_name: str
    subject_id: int
    teacher_id: int
    room_number: str
    day_of_week: str
    start_time: str
    end_time: str
    marhala_id: int
    academic_year: str
    semester: Optional[str] = None

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassSchedule(ClassScheduleBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StudentProgressBase(BaseModel):
    student_id: int
    subject_id: int
    marks_obtained: float
    grade: str
    attendance_percentage: float
    teacher_remarks: Optional[str] = None
    exam_type: str  # monthly, quarterly, final
    exam_date: str

class StudentProgressCreate(StudentProgressBase):
    pass

class StudentProgress(StudentProgressBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TeacherAssignmentBase(BaseModel):
    teacher_id: int
    subject_id: int
    marhala_id: int
    class_assigned: str
    academic_year: str
    role: str  # main_teacher, assistant_teacher, substitute

class TeacherAssignmentCreate(TeacherAssignmentBase):
    pass

class TeacherAssignment(TeacherAssignmentBase):
    id: int
    assigned_by: int
    assigned_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CurriculumBase(BaseModel):
    name: str
    marhala_id: int
    academic_year: str
    description: Optional[str] = None
    total_subjects: int
    total_credit_hours: int
    passing_criteria: str
    is_active: bool

class CurriculumCreate(CurriculumBase):
    subject_ids: List[int]  # List of subject IDs included in curriculum

class Curriculum(CurriculumBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    subjects: List[Subject] = []

    class Config:
        from_attributes = True

class UserInfo(BaseModel):
    id: int
    email: str
    user_type: str
    permissions: List[str]

# Talim Tarbiat Models
class TalimTarbiatBase(BaseModel):
    name: str
    father_name: str
    mother_name: str

class TalimTarbiatCreate(TalimTarbiatBase):
    pass

class TalimTarbiat(TalimTarbiatBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Request/Response Models for API
class TalimTarbiateRequest(BaseModel):
    name: str
    father_name: str
    mother_name: str

class TalimTarbiateResponse(BaseModel):
    id: int
    name: str
    father_name: str
    mother_name: str
    status: str
    message: str

# Authentication Dependency
async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Get current user - either from gateway headers or direct token validation"""
    
    # Check if request comes from API Gateway (has gateway user headers)
    if request.headers.get('x-authenticated-by') == 'gateway':
        logger.info("Request authenticated by API Gateway")
        
        user_id = request.headers.get('x-user-id')
        user_email = request.headers.get('x-user-email')
        user_type = request.headers.get('x-user-type')
        user_permissions = request.headers.get('x-user-permissions', '').split(',')
        
        if not user_id or not user_email:
            logger.error("Missing user data in gateway headers")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication from gateway"
            )
        
        return UserInfo(
            id=int(user_id),
            email=user_email,
            user_type=user_type,
            permissions=[p.strip() for p in user_permissions if p.strip()]
        )
    
    # Direct authentication (when not via gateway)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/users/auth/validate/",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )

            if response.status_code != 200:
                logger.error(f"Auth validation failed: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )

            data = response.json()
            
            if not data.get('valid', False):
                logger.error(f"Token validation failed: {data.get('error', 'Unknown error')}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=data.get('error', 'Invalid authentication credentials')
                )

            user_data = data.get('user')
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User data not found in response"
                )

            return UserInfo(**user_data)

    except httpx.RequestError as e:
        logger.error(f"Auth service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )

# Permission Check
async def require_admin_permission(
    request: Request,
    current_user: UserInfo = Depends(get_current_user)
):
    """Require admin permissions"""
    if 'admin' not in current_user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permissions required"
        )
    return current_user

# Database Connection
class Database:
    """PostgreSQL database connection manager using asyncpg"""
    def __init__(self):
        self.db_url = DATABASE_URL
        self.pool = None

    async def create_pool(self):
        """Create connection pool"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                self.db_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created successfully")

    async def execute_query(self, query: str, params: dict = None):
        """Execute database query and return results"""
        if not self.pool:
            await self.create_pool()

        async with self.pool.acquire() as connection:
            if params:
                result = await connection.fetch(query, *params.values())
            else:
                result = await connection.fetch(query)
            return result

    async def execute_insert(self, query: str, params: dict = None):
        """Execute INSERT query and return the created record"""
        if not self.pool:
            await self.create_pool()

        async with self.pool.acquire() as connection:
            if params:
                result = await connection.fetchrow(query, *params.values())
            else:
                result = await connection.fetchrow(query)
            return result

    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

db = Database()

# API Routes

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "taleem-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

# Talim Tarbiat Endpoints
@app.post("/api/taleem/talim-tarbiat/", response_model=TalimTarbiateResponse)
async def create_talim_tarbiat(request: Request, talim_data: TalimTarbiateRequest, current_user: UserInfo = Depends(get_current_user)):
    """Create Talim Tarbiat entry"""
    logger.info("Request authenticated by API Gateway")
    logger.info(f"Creating Talim Tarbiat entry: {talim_data.dict()}")
    
    try:
        # Insert into database
        insert_query = """
        INSERT INTO talim_tarbiat (name, father_name, mother_name)
        VALUES ($1, $2, $3)
        RETURNING id, name, father_name, mother_name;
        """
        
        params = {
            "name": talim_data.name,
            "father_name": talim_data.father_name,
            "mother_name": talim_data.mother_name
        }
        
        result = await db.execute_insert(insert_query, params)
        
        if result:
            logger.info(f"Created Talim Tarbiat entry with ID: {result['id']}")
            
            return TalimTarbiateResponse(
                id=result["id"],
                name=result["name"],
                father_name=result["father_name"],
                mother_name=result["mother_name"],
                status="success",
                message="Talim Tarbiat entry created successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create Talim Tarbiat entry"
            )
            
    except Exception as e:
        logger.error(f"Error creating Talim Tarbiat entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.get("/api/taleem/talim-tarbiat/", response_model=List[TalimTarbiat])
async def get_talim_tarbiat_entries(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of Talim Tarbiat entries"""
    try:
        logger.info(f"Fetching Talim Tarbiat entries for user {current_user.id}")
        
        # For demo, return empty list
        # In real implementation, execute database query
        return []

    except Exception as e:
        logger.error(f"Error fetching Talim Tarbiat entries: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch Talim Tarbiat entries"
        )

# Subject Management
@app.get("/api/taleem/subjects/", response_model=List[Subject])
async def get_subjects(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    marhala_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of subjects"""
    try:
        # Database query would go here
        # For demo, return empty list
        return []

    except Exception as e:
        logger.error(f"Error fetching subjects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch subjects"
        )

@app.post("/api/taleem/subjects/", response_model=Subject)
async def create_subject(
    request: Request,
    subject: SubjectCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new subject"""
    try:
        # Insert subject into database
        query = """
        INSERT INTO subjects (name, name_bangla, code, description, marhala_id,
                             class_type, credit_hours, passing_marks, total_marks,
                             is_active, created_by)
        VALUES (%(name)s, %(name_bangla)s, %(code)s, %(description)s, %(marhala_id)s,
                %(class_type)s, %(credit_hours)s, %(passing_marks)s, %(total_marks)s,
                true, %(created_by)s)
        RETURNING id, created_at, updated_at
        """

        params = {
            "name": subject.name,
            "name_bangla": subject.name_bangla,
            "code": subject.code,
            "description": subject.description,
            "marhala_id": subject.marhala_id,
            "class_type": subject.class_type,
            "credit_hours": subject.credit_hours,
            "passing_marks": subject.passing_marks,
            "total_marks": subject.total_marks,
            "created_by": current_user.id
        }

        # Execute database query
        result = await db.execute_query(query, params)

        # Return created subject (mock response)
        return Subject(
            id=1,
            **subject.dict(),
            is_active=True,
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating subject: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create subject"
        )

@app.get("/api/taleem/subjects/{subject_id}", response_model=Subject)
async def get_subject(
    request: Request,
    subject_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get specific subject by ID"""
    try:
        # Database query would go here
        # For demo, raise not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching subject {subject_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch subject"
        )

@app.put("/api/taleem/subjects/{subject_id}", response_model=Subject)
async def update_subject(
    request: Request,
    subject_id: int,
    subject: SubjectUpdate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Update existing subject"""
    try:
        # Update subject in database
        # For demo, return success response
        return Subject(
            id=subject_id,
            name=subject.name or "Mathematics",
            name_bangla=subject.name_bangla or "গণিত",
            code=subject.code or "MATH101",
            description=subject.description or "Basic Mathematics",
            marhala_id=1,
            class_type=subject.class_type or "theory",
            credit_hours=subject.credit_hours or 3,
            passing_marks=subject.passing_marks or 40,
            total_marks=subject.total_marks or 100,
            is_active=True,
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error updating subject {subject_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update subject"
        )

# Class Schedule Management
@app.get("/api/taleem/schedules/", response_model=List[ClassSchedule])
async def get_class_schedules(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    marhala_id: Optional[int] = None,
    day_of_week: Optional[str] = None,
    academic_year: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of class schedules"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching class schedules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch class schedules"
        )

@app.post("/api/taleem/schedules/", response_model=ClassSchedule)
async def create_class_schedule(
    request: Request,
    schedule: ClassScheduleCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new class schedule"""
    try:
        # Insert schedule into database
        return ClassSchedule(
            id=1,
            **schedule.dict(),
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating class schedule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create class schedule"
        )

# Student Progress Management
@app.get("/api/taleem/progress/", response_model=List[StudentProgress])
async def get_student_progress(
    skip: int = 0,
    limit: int = 20,
    student_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    exam_type: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of student progress records"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching student progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch student progress"
        )

@app.post("/api/taleem/progress/", response_model=StudentProgress)
async def create_student_progress(
    request: Request,
    progress: StudentProgressCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new student progress record"""
    try:
        # Insert progress record into database
        return StudentProgress(
            id=1,
            **progress.dict(),
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating student progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create student progress"
        )

@app.get("/api/taleem/progress/student/{student_id}", response_model=List[StudentProgress])
async def get_student_progress_by_student(
    student_id: int,
    academic_year: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get progress records for a specific student"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching progress for student {student_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch student progress"
        )

# Teacher Assignment Management
@app.get("/api/taleem/teacher-assignments/", response_model=List[TeacherAssignment])
async def get_teacher_assignments(
    skip: int = 0,
    limit: int = 20,
    teacher_id: Optional[int] = None,
    marhala_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of teacher assignments"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching teacher assignments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch teacher assignments"
        )

@app.post("/api/taleem/teacher-assignments/", response_model=TeacherAssignment)
async def create_teacher_assignment(
    request: Request,
    assignment: TeacherAssignmentCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new teacher assignment"""
    try:
        # Insert assignment into database
        return TeacherAssignment(
            id=1,
            **assignment.dict(),
            assigned_by=current_user.id,
            assigned_date=datetime.now(),
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating teacher assignment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create teacher assignment"
        )

# Curriculum Management
@app.get("/api/taleem/curricula/", response_model=List[Curriculum])
async def get_curricula(
    skip: int = 0,
    limit: int = 20,
    marhala_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of curricula"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching curricula: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch curricula"
        )

@app.post("/api/taleem/curricula/", response_model=Curriculum)
async def create_curriculum(
    request: Request,
    curriculum: CurriculumCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new curriculum"""
    try:
        # Insert curriculum into database
        return Curriculum(
            id=1,
            name=curriculum.name,
            marhala_id=curriculum.marhala_id,
            academic_year=curriculum.academic_year,
            description=curriculum.description,
            total_subjects=len(curriculum.subject_ids),
            total_credit_hours=0,  # Calculate from subjects
            passing_criteria=curriculum.passing_criteria,
            is_active=curriculum.is_active,
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            subjects=[]
        )

    except Exception as e:
        logger.error(f"Error creating curriculum: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create curriculum"
        )

# Reports and Analytics
@app.get("/api/taleem/reports/academic-performance")
async def get_academic_performance_report(
    marhala_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    class_name: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Generate academic performance report"""
    try:
        # Generate academic performance report
        return {
            "summary": {
                "total_students": 0,
                "average_marks": 0.0,
                "pass_rate": 0.0,
                "grade_distribution": {}
            },
            "by_subject": {},
            "by_class": {},
            "filters": {
                "marhala_id": marhala_id,
                "academic_year": academic_year,
                "class_name": class_name
            }
        }

    except Exception as e:
        logger.error(f"Error generating academic performance report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate academic performance report"
        )

@app.get("/api/taleem/reports/teacher-workload")
async def get_teacher_workload_report(
    academic_year: Optional[str] = None,
    marhala_id: Optional[int] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Generate teacher workload report"""
    try:
        # Generate teacher workload report
        return {
            "teachers": [],
            "summary": {
                "total_teachers": 0,
                "average_classes_per_teacher": 0.0,
                "total_hours_assigned": 0
            },
            "filters": {
                "academic_year": academic_year,
                "marhala_id": marhala_id
            }
        }

    except Exception as e:
        logger.error(f"Error generating teacher workload report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate teacher workload report"
        )

@app.get("/api/taleem/reports/attendance")
async def get_attendance_report(
    marhala_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    month: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Generate attendance report"""
    try:
        # Generate attendance report
        return {
            "summary": {
                "total_students": 0,
                "average_attendance": 0.0,
                "attendance_rate": 0.0
            },
            "by_class": {},
            "by_subject": {},
            "monthly_trends": {},
            "filters": {
                "marhala_id": marhala_id,
                "academic_year": academic_year,
                "month": month
            }
        }

    except Exception as e:
        logger.error(f"Error generating attendance report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate attendance report"
        )

@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables"""
    try:
        await db.create_pool()
        
        # Create talim_tarbiat table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS talim_tarbiat (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            father_name VARCHAR(255) NOT NULL,
            mother_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        async with db.pool.acquire() as connection:
            await connection.execute(create_table_query)
            logger.info("Database tables created/verified successfully")
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections"""
    await db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
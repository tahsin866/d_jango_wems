from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Union
import httpx
import os
from datetime import datetime, date
import uuid
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import json
from enum import Enum as PyEnum

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/wifaq")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
TRAINING_UPLOAD_DIR = "/app/uploads"

# FastAPI App
app = FastAPI(title="Training Service", version="1.0.0", description="Training Programs and Materials Management Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Security
security = HTTPBearer()

# Create upload directory
os.makedirs(TRAINING_UPLOAD_DIR, exist_ok=True)

# Enums
class TrainingStatus(PyEnum):
    draft = "draft"
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"

class EnrollmentStatus(PyEnum):
    registered = "registered"
    attending = "attending"
    completed = "completed"
    dropped = "dropped"
    certified = "certified"

class MaterialType(PyEnum):
    document = "document"
    video = "video"
    audio = "audio"
    presentation = "presentation"
    image = "image"
    other = "other"

# Database Models
class TrainingProgram(Base):
    __tablename__ = 'training_programs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    description = Column(Text)
    description_bangla = Column(Text)
    objectives = Column(Text)
    objectives_bangla = Column(Text)
    training_type = Column(String(100))  # workshop, seminar, course, certification
    category = Column(String(100))
    target_audience = Column(String(255))
    prerequisites = Column(Text)
    prerequisites_bangla = Column(Text)
    duration_hours = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String(255))
    online_platform = Column(String(255))
    max_participants = Column(Integer)
    min_participants = Column(Integer)
    registration_deadline = Column(DateTime)
    fee = Column(Numeric(10, 2), default=0)
    certificate_issued = Column(Boolean, default=False)
    status = Column(Enum(TrainingStatus), default=TrainingStatus.draft)
    instructor_id = Column(Integer)
    coordinator_id = Column(Integer)
    madrasha_id = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrainingEnrollment(Base):
    __tablename__ = 'training_enrollments'

    id = Column(Integer, primary_key=True, index=True)
    training_program_id = Column(Integer, ForeignKey('training_programs.id'), nullable=False)
    participant_id = Column(Integer, nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.registered)
    completion_date = Column(DateTime)
    grade = Column(String(10))
    score = Column(Numeric(5, 2))
    certificate_id = Column(Integer)
    notes = Column(Text)
    approved_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrainingMaterial(Base):
    __tablename__ = 'training_materials'

    id = Column(Integer, primary_key=True, index=True)
    training_program_id = Column(Integer, ForeignKey('training_programs.id'), nullable=False)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    description = Column(Text)
    description_bangla = Column(Text)
    material_type = Column(Enum(MaterialType))
    file_path = Column(String(500))
    file_size = Column(Integer)
    download_count = Column(Integer, default=0)
    order_index = Column(Integer)
    is_required = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    uploaded_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrainingSchedule(Base):
    __tablename__ = 'training_schedules'

    id = Column(Integer, primary_key=True, index=True)
    training_program_id = Column(Integer, ForeignKey('training_programs.id'), nullable=False)
    session_title = Column(String(255))
    session_title_bangla = Column(String(255))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(255))
    online_meeting_link = Column(String(500))
    instructor_id = Column(Integer)
    topics = Column(Text)
    topics_bangla = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrainingAssessment(Base):
    __tablename__ = 'training_assessments'

    id = Column(Integer, primary_key=True, index=True)
    training_program_id = Column(Integer, ForeignKey('training_programs.id'), nullable=False)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    assessment_type = Column(String(50))  # quiz, assignment, project, exam, presentation
    max_score = Column(Numeric(5, 2))
    passing_score = Column(Numeric(5, 2))
    duration_minutes = Column(Integer)
    instructions = Column(Text)
    instructions_bangla = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrainingCertificate(Base):
    __tablename__ = 'training_certificates'

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey('training_enrollments.id'), nullable=False)
    certificate_number = Column(String(100), unique=True, index=True)
    issue_date = Column(DateTime, default=datetime.utcnow)
    certificate_template = Column(String(255))
    signatory_name = Column(String(255))
    signatory_title = Column(String(255))
    additional_text = Column(Text)
    file_path = Column(String(500))
    qr_code_path = Column(String(500))
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class TrainingProgramBase(BaseModel):
    title: str
    title_bangla: Optional[str] = None
    description: Optional[str] = None
    description_bangla: Optional[str] = None
    objectives: Optional[str] = None
    objectives_bangla: Optional[str] = None
    training_type: str
    category: Optional[str] = None
    target_audience: Optional[str] = None
    prerequisites: Optional[str] = None
    prerequisites_bangla: Optional[str] = None
    duration_hours: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    online_platform: Optional[str] = None
    max_participants: Optional[int] = None
    min_participants: Optional[int] = None
    registration_deadline: Optional[str] = None
    fee: float = 0
    certificate_issued: bool = False
    instructor_id: Optional[int] = None
    coordinator_id: Optional[int] = None
    madrasha_id: int

class TrainingProgramCreate(TrainingProgramBase):
    pass

class TrainingProgramUpdate(BaseModel):
    title: Optional[str] = None
    title_bangla: Optional[str] = None
    description: Optional[str] = None
    description_bangla: Optional[str] = None
    objectives: Optional[str] = None
    objectives_bangla: Optional[str] = None
    training_type: Optional[str] = None
    category: Optional[str] = None
    target_audience: Optional[str] = None
    prerequisites: Optional[str] = None
    prerequisites_bangla: Optional[str] = None
    duration_hours: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    online_platform: Optional[str] = None
    max_participants: Optional[int] = None
    min_participants: Optional[int] = None
    registration_deadline: Optional[str] = None
    fee: Optional[float] = None
    certificate_issued: Optional[bool] = None
    instructor_id: Optional[int] = None
    coordinator_id: Optional[int] = None
    status: Optional[TrainingStatus] = None

class TrainingProgramResponse(TrainingProgramBase):
    id: int
    status: TrainingStatus
    created_by: int
    created_at: datetime
    updated_at: datetime

class TrainingEnrollmentBase(BaseModel):
    training_program_id: int
    participant_id: int
    notes: Optional[str] = None

class TrainingEnrollmentCreate(TrainingEnrollmentBase):
    pass

class TrainingEnrollmentResponse(TrainingEnrollmentBase):
    id: int
    enrollment_date: datetime
    status: EnrollmentStatus
    completion_date: Optional[datetime] = None
    grade: Optional[str] = None
    score: Optional[float] = None
    certificate_id: Optional[int] = None
    approved_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class TrainingMaterialBase(BaseModel):
    training_program_id: int
    title: str
    title_bangla: Optional[str] = None
    description: Optional[str] = None
    description_bangla: Optional[str] = None
    material_type: MaterialType
    order_index: int = 0
    is_required: bool = False

class TrainingMaterialCreate(TrainingMaterialBase):
    pass

class TrainingMaterialResponse(TrainingMaterialBase):
    id: int
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    download_count: int
    is_active: bool
    uploaded_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class TrainingScheduleBase(BaseModel):
    training_program_id: int
    session_title: str
    session_title_bangla: Optional[str] = None
    start_time: str
    end_time: str
    location: Optional[str] = None
    online_meeting_link: Optional[str] = None
    instructor_id: Optional[int] = None
    topics: Optional[str] = None
    topics_bangla: Optional[str] = None

class TrainingScheduleCreate(TrainingScheduleBase):
    pass

class TrainingScheduleResponse(TrainingScheduleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class TrainingAssessmentBase(BaseModel):
    training_program_id: int
    title: str
    title_bangla: Optional[str] = None
    assessment_type: str
    max_score: float
    passing_score: float
    duration_minutes: Optional[int] = None
    instructions: Optional[str] = None
    instructions_bangla: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class TrainingAssessmentCreate(TrainingAssessmentBase):
    pass

class TrainingAssessmentResponse(TrainingAssessmentBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/auth/validate/",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Authentication service unavailable")

async def require_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") not in ["master_admin", "super_admin", "board_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Database initialization
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Helper functions
async def save_upload_file(upload_file: UploadFile, directory: str) -> str:
    file_extension = upload_file.filename.split('.')[-1] if '.' in upload_file.filename else ''
    filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(directory, filename)

    async with aiofiles.open(file_path, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)

    return file_path

def generate_certificate_number(training_id: int, participant_id: int) -> str:
    return f"TRN-{training_id:06d}-{participant_id:06d}-{datetime.now().year}"

def generate_verification_code() -> str:
    return uuid.uuid4().hex[:12].upper()

# Training Program Endpoints
@app.post("/programs", response_model=TrainingProgramResponse)
async def create_training_program(
    program: TrainingProgramCreate,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_program = TrainingProgram(**program.dict(), created_by=current_user["id"])
    db.add(db_program)
    await db.commit()
    await db.refresh(db_program)
    return db_program

@app.get("/programs", response_model=List[TrainingProgramResponse])
async def get_training_programs(
    skip: int = 0,
    limit: int = 100,
    training_type: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[TrainingStatus] = None,
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingProgram)

    if madrasha_id or current_user.get("role") == "madrasha":
        query = query.where(TrainingProgram.madrasha_id == (madrasha_id or current_user.get("madrasha_id")))

    if training_type:
        query = query.where(TrainingProgram.training_type == training_type)
    if category:
        query = query.where(TrainingProgram.category == category)
    if status:
        query = query.where(TrainingProgram.status == status)

    query = query.order_by(TrainingProgram.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/programs/{program_id}", response_model=TrainingProgramResponse)
async def get_training_program(
    program_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingProgram).where(TrainingProgram.id == program_id)
    result = await db.execute(query)
    program = result.scalar_one_or_none()

    if not program:
        raise HTTPException(status_code=404, detail="Training program not found")

    return program

@app.put("/programs/{program_id}", response_model=TrainingProgramResponse)
async def update_training_program(
    program_id: int,
    program_update: TrainingProgramUpdate,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingProgram).where(TrainingProgram.id == program_id)
    result = await db.execute(query)
    program = result.scalar_one_or_none()

    if not program:
        raise HTTPException(status_code=404, detail="Training program not found")

    update_data = program_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(program, field, value)

    await db.commit()
    await db.refresh(program)
    return program

# Training Enrollment Endpoints
@app.post("/enrollments", response_model=TrainingEnrollmentResponse)
async def create_enrollment(
    enrollment: TrainingEnrollmentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if program exists and is open for registration
    program_query = select(TrainingProgram).where(TrainingProgram.id == enrollment.training_program_id)
    program_result = await db.execute(program_query)
    program = program_result.scalar_one_or_none()

    if not program:
        raise HTTPException(status_code=404, detail="Training program not found")

    if program.registration_deadline and datetime.now() > program.registration_deadline:
        raise HTTPException(status_code=400, detail="Registration deadline has passed")

    if program.max_participants:
        current_enrollments_query = select(TrainingEnrollment).where(
            TrainingEnrollment.training_program_id == enrollment.training_program_id,
            TrainingEnrollment.status.in_([EnrollmentStatus.registered, EnrollmentStatus.attending])
        )
        current_enrollments_result = await db.execute(current_enrollments_query)
        current_count = len(current_enrollments_result.scalars().all())

        if current_count >= program.max_participants:
            raise HTTPException(status_code=400, detail="Training program is full")

    db_enrollment = TrainingEnrollment(**enrollment.dict())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    return db_enrollment

@app.get("/enrollments", response_model=List[TrainingEnrollmentResponse])
async def get_enrollments(
    skip: int = 0,
    limit: int = 100,
    training_program_id: Optional[int] = None,
    participant_id: Optional[int] = None,
    status: Optional[EnrollmentStatus] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingEnrollment)

    if training_program_id:
        query = query.where(TrainingEnrollment.training_program_id == training_program_id)
    if participant_id:
        query = query.where(TrainingEnrollment.participant_id == participant_id)
    if status:
        query = query.where(TrainingEnrollment.status == status)

    query = query.order_by(TrainingEnrollment.enrollment_date.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Training Material Endpoints
@app.post("/materials", response_model=TrainingMaterialResponse)
async def create_training_material(
    material: TrainingMaterialCreate,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_material = TrainingMaterial(**material.dict(), uploaded_by=current_user["id"])
    db.add(db_material)
    await db.commit()
    await db.refresh(db_material)
    return db_material

@app.post("/materials/{material_id}/upload")
async def upload_material_file(
    material_id: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingMaterial).where(TrainingMaterial.id == material_id)
    result = await db.execute(query)
    material = result.scalar_one_or_none()

    if not material:
        raise HTTPException(status_code=404, detail="Training material not found")

    file_path = await save_upload_file(file, TRAINING_UPLOAD_DIR)

    material.file_path = file_path
    material.file_size = len(await file.read())
    await file.seek(0)  # Reset file pointer
    await db.commit()

    return {"message": "File uploaded successfully", "file_path": file_path}

@app.get("/materials", response_model=List[TrainingMaterialResponse])
async def get_training_materials(
    skip: int = 0,
    limit: int = 100,
    training_program_id: Optional[int] = None,
    material_type: Optional[MaterialType] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingMaterial).where(TrainingMaterial.is_active == True)

    if training_program_id:
        query = query.where(TrainingMaterial.training_program_id == training_program_id)
    if material_type:
        query = query.where(TrainingMaterial.material_type == material_type)

    query = query.order_by(TrainingMaterial.order_index).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Training Schedule Endpoints
@app.post("/schedules", response_model=TrainingScheduleResponse)
async def create_training_schedule(
    schedule: TrainingScheduleCreate,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_schedule = TrainingSchedule(**schedule.dict())
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule

@app.get("/schedules", response_model=List[TrainingScheduleResponse])
async def get_training_schedules(
    skip: int = 0,
    limit: int = 100,
    training_program_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingSchedule).where(TrainingSchedule.is_active == True)

    if training_program_id:
        query = query.where(TrainingSchedule.training_program_id == training_program_id)

    query = query.order_by(TrainingSchedule.start_time).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Training Assessment Endpoints
@app.post("/assessments", response_model=TrainingAssessmentResponse)
async def create_training_assessment(
    assessment: TrainingAssessmentCreate,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_assessment = TrainingAssessment(**assessment.dict(), created_by=current_user["id"])
    db.add(db_assessment)
    await db.commit()
    await db.refresh(db_assessment)
    return db_assessment

@app.get("/assessments", response_model=List[TrainingAssessmentResponse])
async def get_training_assessments(
    skip: int = 0,
    limit: int = 100,
    training_program_id: Optional[int] = None,
    assessment_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TrainingAssessment).where(TrainingAssessment.is_active == True)

    if training_program_id:
        query = query.where(TrainingAssessment.training_program_id == training_program_id)
    if assessment_type:
        query = query.where(TrainingAssessment.assessment_type == assessment_type)

    query = query.order_by(TrainingAssessment.created_at).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Certificate Endpoints
@app.post("/certificates/generate/{enrollment_id}")
async def generate_certificate(
    enrollment_id: int,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Get enrollment
    enrollment_query = select(TrainingEnrollment).where(TrainingEnrollment.id == enrollment_id)
    enrollment_result = await db.execute(enrollment_query)
    enrollment = enrollment_result.scalar_one_or_none()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    if enrollment.status != EnrollmentStatus.completed:
        raise HTTPException(status_code=400, detail="Participant must complete training to receive certificate")

    # Check if certificate already exists
    existing_cert_query = select(TrainingCertificate).where(TrainingCertificate.enrollment_id == enrollment_id)
    existing_cert_result = await db.execute(existing_cert_query)
    existing_cert = existing_cert_result.scalar_one_or_none()

    if existing_cert:
        return {"message": "Certificate already generated", "certificate_id": existing_cert.id}

    # Generate certificate
    certificate_number = generate_certificate_number(enrollment.training_program_id, enrollment.participant_id)
    verification_code = generate_verification_code()

    db_certificate = TrainingCertificate(
        enrollment_id=enrollment_id,
        certificate_number=certificate_number,
        verification_code=verification_code
    )
    db.add(db_certificate)
    await db.commit()
    await db.refresh(db_certificate)

    # Update enrollment
    enrollment.certificate_id = db_certificate.id
    enrollment.status = EnrollmentStatus.certified
    await db.commit()

    return {"message": "Certificate generated successfully", "certificate_id": db_certificate.id}

@app.get("/certificates/verify/{verification_code}")
async def verify_certificate(verification_code: str, db: AsyncSession = Depends(get_db)):
    query = select(TrainingCertificate).where(TrainingCertificate.verification_code == verification_code)
    result = await db.execute(query)
    certificate = result.scalar_one_or_none()

    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # Mark as verified
    if not certificate.is_verified:
        certificate.is_verified = True
        await db.commit()

    return {
        "certificate_number": certificate.certificate_number,
        "issue_date": certificate.issue_date,
        "is_verified": True
    }

# Statistics Endpoints
@app.get("/statistics")
async def get_training_statistics(
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if madrasha_id or current_user.get("role") == "madrasha":
        madrasha_id = madrasha_id or current_user.get("madrasha_id")

    # Count training programs
    programs_query = select(TrainingProgram).where(TrainingProgram.madrasha_id == madrasha_id)
    programs_result = await db.execute(programs_query)
    total_programs = len(programs_result.scalars().all())

    # Count active enrollments
    enrollments_query = select(TrainingEnrollment).join(TrainingProgram).where(
        TrainingProgram.madrasha_id == madrasha_id,
        TrainingEnrollment.status.in_([EnrollmentStatus.registered, EnrollmentStatus.attending])
    )
    enrollments_result = await db.execute(enrollments_query)
    active_enrollments = len(enrollments_result.scalars().all())

    # Count completed certifications
    certified_query = select(TrainingEnrollment).join(TrainingProgram).where(
        TrainingProgram.madrasha_id == madrasha_id,
        TrainingEnrollment.status == EnrollmentStatus.certified
    )
    certified_result = await db.execute(certified_query)
    total_certified = len(certified_result.scalars().all())

    # Count training materials
    materials_query = select(TrainingMaterial).join(TrainingProgram).where(
        TrainingProgram.madrasha_id == madrasha_id,
        TrainingMaterial.is_active == True
    )
    materials_result = await db.execute(materials_query)
    total_materials = len(materials_result.scalars().all())

    return {
        "total_programs": total_programs,
        "active_enrollments": active_enrollments,
        "total_certified": total_certified,
        "total_materials": total_materials
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "training-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
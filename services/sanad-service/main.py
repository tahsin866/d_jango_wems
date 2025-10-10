"""
FastAPI Certificate (Sanad) Service
Handles certificate generation, Sanad management, certificate verification, and document templates.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import httpx
import os
from datetime import datetime
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WEMS Certificate (Sanad) Service",
    description="Certificate generation and verification management service",
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
CERTIFICATE_STORAGE_PATH = os.getenv("CERTIFICATE_STORAGE_PATH", "/app/certificates")
TEMPLATE_STORAGE_PATH = os.getenv("TEMPLATE_STORAGE_PATH", "/app/templates")

# Security
security = HTTPBearer()

# Pydantic Models
class CertificateBase(BaseModel):
    certificate_type: str  # sanad, merit_certificate, attendance_certificate, completion_certificate
    student_id: int
    madrasha_id: int
    marhala_id: int
    academic_year: str
    exam_roll: str
    result_gpa: Optional[float] = None
    result_grade: Optional[str] = None
    passing_year: Optional[int] = None
    board_name: Optional[str] = None
    student_name_bangla: str
    student_name_english: str
    father_name: str
    mother_name: str
    date_of_birth: str
    registration_number: str

class CertificateCreate(CertificateBase):
    template_id: Optional[int] = None
    issuing_authority: str
    issue_date: str
    certificate_number: Optional[str] = None

class CertificateUpdate(BaseModel):
    certificate_type: Optional[str] = None
    result_gpa: Optional[float] = None
    result_grade: Optional[str] = None
    passing_year: Optional[int] = None
    board_name: Optional[str] = None
    issuing_authority: Optional[str] = None
    issue_date: Optional[str] = None

class Certificate(CertificateBase):
    id: int
    template_id: Optional[int] = None
    issuing_authority: str
    issue_date: str
    certificate_number: str
    verification_code: str
    status: str  # draft, issued, verified, revoked
    pdf_path: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    issued_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CertificateTemplateBase(BaseModel):
    name: str
    certificate_type: str
    marhala_id: int
    description: Optional[str] = None
    background_color: str = "#ffffff"
    text_color: str = "#000000"
    border_color: str = "#gold"
    font_family: str = "Arial"
    logo_path: Optional[str] = None
    signature_path_1: Optional[str] = None
    signature_path_2: Optional[str] = None
    watermark_path: Optional[str] = None
    dimensions_width: int = 794  # A4 width in points
    dimensions_height: int = 1123  # A4 height in points

class CertificateTemplateCreate(CertificateTemplateBase):
    html_template: str  # HTML template for certificate
    css_styles: Optional[str] = None

class CertificateTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    border_color: Optional[str] = None
    font_family: Optional[str] = None
    html_template: Optional[str] = None
    css_styles: Optional[str] = None

class CertificateTemplate(CertificateTemplateBase):
    id: int
    html_template: str
    css_styles: Optional[str] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CertificateVerification(BaseModel):
    certificate_number: str
    verification_code: str
    student_name: str
    certificate_type: str
    issuing_madrasha: str
    marhala: str
    academic_year: str
    result_gpa: Optional[float] = None
    result_grade: Optional[str] = None
    issue_date: str
    status: str
    verification_date: datetime

class CertificateGenerationRequest(BaseModel):
    certificate_type: str
    template_id: int
    student_ids: List[int]
    academic_year: str
    issuing_authority: str
    issue_date: str

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
                    "service_name": "sanad-service"
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

# Utility Functions
def generate_certificate_number(certificate_type: str, madrasha_id: int, year: str) -> str:
    """Generate unique certificate number"""
    return f"{certificate_type.upper()}-{madrasha_id:06d}-{year}-{uuid.uuid4().hex[:8].upper()}"

def generate_verification_code() -> str:
    """Generate verification code"""
    return uuid.uuid4().hex[:12].upper()

# API Routes

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sanad-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

# Certificate Management
@app.get("/api/sanad/certificates/", response_model=List[Certificate])
async def get_certificates(
    skip: int = 0,
    limit: int = 20,
    certificate_type: Optional[str] = None,
    madrasha_id: Optional[int] = None,
    marhala_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    status: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of certificates"""
    try:
        # Database query would go here
        # For demo, return empty list
        return []

    except Exception as e:
        logger.error(f"Error fetching certificates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch certificates"
        )

@app.post("/api/sanad/certificates/", response_model=Certificate)
async def create_certificate(
    certificate: CertificateCreate,
    current_user: UserInfo = Depends(require_permission("certificate_create"))
):
    """Create a new certificate"""
    try:
        # Generate certificate number and verification code
        certificate_number = certificate.certificate_number or generate_certificate_number(
            certificate.certificate_type,
            certificate.madrasha_id,
            certificate.academic_year
        )
        verification_code = generate_verification_code()

        # Insert certificate into database
        query = """
        INSERT INTO certificates (certificate_type, student_id, madrasha_id, marhala_id,
                                academic_year, exam_roll, result_gpa, result_grade,
                                passing_year, board_name, student_name_bangla,
                                student_name_english, father_name, mother_name,
                                date_of_birth, registration_number, template_id,
                                issuing_authority, issue_date, certificate_number,
                                verification_code, status, created_by)
        VALUES (%(certificate_type)s, %(student_id)s, %(madrasha_id)s, %(marhala_id)s,
                %(academic_year)s, %(exam_roll)s, %(result_gpa)s, %(result_grade)s,
                %(passing_year)s, %(board_name)s, %(student_name_bangla)s,
                %(student_name_english)s, %(father_name)s, %(mother_name)s,
                %(date_of_birth)s, %(registration_number)s, %(template_id)s,
                %(issuing_authority)s, %(issue_date)s, %(certificate_number)s,
                %(verification_code)s, 'draft', %(created_by)s)
        RETURNING id, created_at, updated_at
        """

        params = {
            "certificate_type": certificate.certificate_type,
            "student_id": certificate.student_id,
            "madrasha_id": certificate.madrasha_id,
            "marhala_id": certificate.marhala_id,
            "academic_year": certificate.academic_year,
            "exam_roll": certificate.exam_roll,
            "result_gpa": certificate.result_gpa,
            "result_grade": certificate.result_grade,
            "passing_year": certificate.passing_year,
            "board_name": certificate.board_name,
            "student_name_bangla": certificate.student_name_bangla,
            "student_name_english": certificate.student_name_english,
            "father_name": certificate.father_name,
            "mother_name": certificate.mother_name,
            "date_of_birth": certificate.date_of_birth,
            "registration_number": certificate.registration_number,
            "template_id": certificate.template_id,
            "issuing_authority": certificate.issuing_authority,
            "issue_date": certificate.issue_date,
            "certificate_number": certificate_number,
            "verification_code": verification_code,
            "created_by": current_user.id
        }

        # Execute database query
        result = await db.execute_query(query, params)

        # Return created certificate (mock response)
        return Certificate(
            id=1,
            **certificate.dict(),
            certificate_number=certificate_number,
            verification_code=verification_code,
            status="draft",
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating certificate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create certificate"
        )

@app.get("/api/sanad/certificates/{certificate_id}", response_model=Certificate)
async def get_certificate(
    certificate_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get specific certificate by ID"""
    try:
        # Database query would go here
        # For demo, raise not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching certificate {certificate_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch certificate"
        )

@app.put("/api/sanad/certificates/{certificate_id}", response_model=Certificate)
async def update_certificate(
    certificate_id: int,
    certificate: CertificateUpdate,
    current_user: UserInfo = Depends(require_permission("certificate_update"))
):
    """Update existing certificate"""
    try:
        # Update certificate in database
        # For demo, return success response
        return Certificate(
            id=certificate_id,
            certificate_type=certificate.certificate_type or "sanad",
            student_id=1,
            madrasha_id=1,
            marhala_id=1,
            academic_year="2024",
            exam_roll="001",
            result_gpa=certificate.result_gpa or 4.5,
            result_grade=certificate.result_grade or "A+",
            passing_year=certificate.passing_year or 2024,
            board_name=certificate.board_name or "Bangladesh Madrasah Education Board",
            student_name_bangla="ছাত্র নাম",
            student_name_english="Student Name",
            father_name="Father Name",
            mother_name="Mother Name",
            date_of_birth="2000-01-01",
            registration_number="REG123456",
            issuing_authority=certificate.issuing_authority or "Principal",
            issue_date=certificate.issue_date or "2024-12-01",
            certificate_number="SANAD-000001-2024-ABC12345",
            verification_code="ABC123456789",
            status="updated",
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error updating certificate {certificate_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update certificate"
        )

@app.post("/api/sanad/certificates/{certificate_id}/issue")
async def issue_certificate(
    certificate_id: int,
    current_user: UserInfo = Depends(require_permission("certificate_issue"))
):
    """Issue a certificate (generate PDF and change status)"""
    try:
        # Generate PDF certificate
        pdf_path = f"{CERTIFICATE_STORAGE_PATH}/certificate_{certificate_id}.pdf"

        # Update certificate status to issued
        return {
            "message": "Certificate issued successfully",
            "certificate_id": certificate_id,
            "pdf_path": pdf_path,
            "issued_at": datetime.now(),
            "issued_by": current_user.id
        }

    except Exception as e:
        logger.error(f"Error issuing certificate {certificate_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to issue certificate"
        )

@app.get("/api/sanad/certificates/{certificate_id}/download")
async def download_certificate(
    certificate_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Download certificate PDF"""
    try:
        pdf_path = f"{CERTIFICATE_STORAGE_PATH}/certificate_{certificate_id}.pdf"

        # Check if PDF exists
        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate PDF not found"
            )

        return FileResponse(
            path=pdf_path,
            filename=f"certificate_{certificate_id}.pdf",
            media_type="application/pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading certificate {certificate_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download certificate"
        )

@app.get("/api/sanad/verify/{verification_code}", response_model=CertificateVerification)
async def verify_certificate(verification_code: str):
    """Verify certificate by verification code (public endpoint)"""
    try:
        # Database query to get certificate by verification code
        # For demo, return verification response
        return CertificateVerification(
            certificate_number="SANAD-000001-2024-ABC12345",
            verification_code=verification_code,
            student_name="Student Name",
            certificate_type="sanad",
            issuing_madrasha="Madrasha Name",
            marhala="Dakhil",
            academic_year="2024",
            result_gpa=4.5,
            result_grade="A+",
            issue_date="2024-12-01",
            status="verified",
            verification_date=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error verifying certificate {verification_code}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify certificate"
        )

# Template Management
@app.get("/api/sanad/templates/", response_model=List[CertificateTemplate])
async def get_certificate_templates(
    skip: int = 0,
    limit: int = 20,
    certificate_type: Optional[str] = None,
    marhala_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of certificate templates"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching certificate templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch certificate templates"
        )

@app.post("/api/sanad/templates/", response_model=CertificateTemplate)
async def create_certificate_template(
    template: CertificateTemplateCreate,
    current_user: UserInfo = Depends(require_permission("template_create"))
):
    """Create a new certificate template"""
    try:
        # Insert template into database
        return CertificateTemplate(
            id=1,
            **template.dict(),
            is_active=True,
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error creating certificate template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create certificate template"
        )

@app.post("/api/sanad/generate-batch")
async def generate_batch_certificates(
    request: CertificateGenerationRequest,
    current_user: UserInfo = Depends(require_permission("certificate_batch_generate"))
):
    """Generate certificates for multiple students at once"""
    try:
        generated_certificates = []

        for student_id in request.student_ids:
            # Create certificate for each student
            cert_number = generate_certificate_number(
                request.certificate_type,
                1,  # madrasha_id would come from student data
                request.academic_year
            )

            generated_certificates.append({
                "student_id": student_id,
                "certificate_number": cert_number,
                "status": "generated"
            })

        return {
            "message": "Batch certificate generation initiated",
            "total_certificates": len(request.student_ids),
            "certificates": generated_certificates,
            "generated_by": current_user.id,
            "generated_at": datetime.now()
        }

    except Exception as e:
        logger.error(f"Error generating batch certificates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate batch certificates"
        )

# Reports
@app.get("/api/sanad/reports/issued-certificates")
async def get_issued_certificates_report(
    madrasha_id: Optional[int] = None,
    marhala_id: Optional[int] = None,
    academic_year: Optional[str] = None,
    certificate_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Generate issued certificates report"""
    try:
        return {
            "certificates": [],
            "summary": {
                "total_certificates": 0,
                "by_type": {},
                "by_marhala": {},
                "by_madrasha": {}
            },
            "filters": {
                "madrasha_id": madrasha_id,
                "marhala_id": marhala_id,
                "academic_year": academic_year,
                "certificate_type": certificate_type,
                "start_date": start_date,
                "end_date": end_date
            }
        }

    except Exception as e:
        logger.error(f"Error generating issued certificates report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate issued certificates report"
        )

@app.get("/api/sanad/reports/verification-requests")
async def get_verification_requests_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Generate certificate verification requests report"""
    try:
        return {
            "verification_requests": [],
            "summary": {
                "total_verifications": 0,
                "successful_verifications": 0,
                "failed_verifications": 0,
                "daily_stats": {}
            },
            "filters": {
                "start_date": start_date,
                "end_date": end_date
            }
        }

    except Exception as e:
        logger.error(f"Error generating verification requests report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate verification requests report"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
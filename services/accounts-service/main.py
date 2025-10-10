"""
FastAPI Accounts Service
Handles financial accounting, vouchers, payments, and financial reporting.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
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
    title="WEMS Accounts Service",
    description="Financial accounting and voucher management service",
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/wifaq")

# Security
security = HTTPBearer()

# Pydantic Models
class ExpenseClaimBase(BaseModel):
    name: str
    father_name: str
    mother_name: str

class ExpenseClaimCreate(ExpenseClaimBase):
    pass

class ExpenseClaim(ExpenseClaimBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

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

class VoucherBase(BaseModel):
    voucher_type: str
    amount: float
    description: str
    reference_number: Optional[str] = None
    date: str
    account_code: str
    debit_account: str
    credit_account: str

class VoucherCreate(VoucherBase):
    pass

class VoucherUpdate(BaseModel):
    voucher_type: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    reference_number: Optional[str] = None
    date: Optional[str] = None
    account_code: Optional[str] = None
    debit_account: Optional[str] = None
    credit_account: Optional[str] = None

class Voucher(VoucherBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    status: str

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    student_id: int
    amount: float
    payment_type: str
    payment_method: str
    reference_number: Optional[str] = None
    description: str
    date: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    created_by: int
    created_at: datetime
    status: str
    transaction_id: Optional[str] = None

    class Config:
        from_attributes = True

class UserInfo(BaseModel):
    id: int
    email: str
    user_type: str
    permissions: List[str]

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
async def require_admin_permission(current_user: UserInfo = Depends(get_current_user)):
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

    async def close_pool(self):
        """Close connection pool"""
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
        "service": "accounts-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/accounts/vouchers/", response_model=List[Voucher])
async def get_vouchers(
    skip: int = 0,
    limit: int = 20,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of vouchers"""
    try:
        # Database query would go here
        # For demo, return empty list
        return []

    except Exception as e:
        logger.error(f"Error fetching vouchers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch vouchers"
        )

@app.post("/api/accounts/vouchers/", response_model=Voucher)
async def create_voucher(
    voucher: VoucherCreate,
    current_user: UserInfo = Depends(require_admin_permission)
):
    """Create a new voucher"""
    try:
        # Validate user permissions
        if 'voucher_create' not in current_user.permissions and 'admin' not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create vouchers"
            )

        # Insert voucher into database
        query = """
        INSERT INTO vouchers (voucher_type, amount, description, reference_number,
                             date, account_code, debit_account, credit_account,
                             created_by, status)
        VALUES (%(voucher_type)s, %(amount)s, %(description)s, %(reference_number)s,
                %(date)s, %(account_code)s, %(debit_account)s, %(credit_account)s,
                %(created_by)s, 'pending')
        RETURNING id, created_at, updated_at, status
        """

        params = {
            "voucher_type": voucher.voucher_type,
            "amount": voucher.amount,
            "description": voucher.description,
            "reference_number": voucher.reference_number,
            "date": voucher.date,
            "account_code": voucher.account_code,
            "debit_account": voucher.debit_account,
            "credit_account": voucher.credit_account,
            "created_by": current_user.id
        }

        # Execute database query
        result = await db.execute_query(query, params)

        # Return created voucher (mock response)
        return Voucher(
            id=1,
            **voucher.dict(),
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="pending"
        )

    except Exception as e:
        logger.error(f"Error creating voucher: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create voucher"
        )

@app.get("/api/accounts/vouchers/{voucher_id}", response_model=Voucher)
async def get_voucher(
    voucher_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get specific voucher by ID"""
    try:
        # Database query would go here
        # For demo, raise not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching voucher {voucher_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch voucher"
        )

@app.put("/api/accounts/vouchers/{voucher_id}", response_model=Voucher)
async def update_voucher(
    voucher_id: int,
    voucher: VoucherUpdate,
    current_user: UserInfo = Depends(require_admin_permission)
):
    """Update existing voucher"""
    try:
        # Update voucher in database
        # For demo, return success response
        return Voucher(
            id=voucher_id,
            voucher_type=voucher.voucher_type or "receipt",
            amount=voucher.amount or 0.0,
            description=voucher.description or "",
            created_by=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="updated"
        )

    except Exception as e:
        logger.error(f"Error updating voucher {voucher_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update voucher"
        )

@app.delete("/api/accounts/vouchers/{voucher_id}")
async def delete_voucher(
    voucher_id: int,
    current_user: UserInfo = Depends(require_admin_permission)
):
    """Delete voucher"""
    try:
        # Delete voucher from database
        # For demo, return success response
        return {"message": "Voucher deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting voucher {voucher_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete voucher"
        )

@app.get("/api/accounts/payments/", response_model=List[Payment])
async def get_payments(
    skip: int = 0,
    limit: int = 20,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of payments"""
    try:
        # Database query would go here
        return []

    except Exception as e:
        logger.error(f"Error fetching payments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch payments"
        )

@app.post("/api/accounts/payments/", response_model=Payment)
async def create_payment(
    payment: PaymentCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new payment"""
    try:
        # Insert payment into database
        return Payment(
            id=1,
            **payment.dict(),
            created_by=current_user.id,
            created_at=datetime.now(),
            status="pending",
            transaction_id="TXN123456"
        )

    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create payment"
        )

# Expense Claims Endpoints
@app.post("/api/accounts/expense-claims/", response_model=ExpenseClaim)
async def create_expense_claim(
    request: Request,
    claim: ExpenseClaimCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """Create a new expense claim"""
    try:
        # Validate input
        if not claim.name.strip() or len(claim.name.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name must be at least 2 characters long"
            )

        if not claim.father_name.strip() or len(claim.father_name.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Father name must be at least 2 characters long"
            )

        if not claim.mother_name.strip() or len(claim.mother_name.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mother name must be at least 2 characters long"
            )

        # Insert expense claim into database
        query = """
        INSERT INTO accounts (name, father_name, mother_name, created_at)
        VALUES ($1, $2, $3, NOW())
        RETURNING id, created_at
        """

        params = [
            claim.name.strip(),
            claim.father_name.strip(),
            claim.mother_name.strip()
        ]

        # Execute database query
        result = await db.execute_insert(query, {"param1": params[0], "param2": params[1], "param3": params[2]})

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create expense claim"
            )

        logger.info(f"Created expense claim with ID: {result['id']}")

        return ExpenseClaim(
            id=result['id'],
            name=claim.name.strip(),
            father_name=claim.father_name.strip(),
            mother_name=claim.mother_name.strip(),
            created_at=result['created_at']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating expense claim: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create expense claim"
        )

@app.get("/api/accounts/expense-claims/", response_model=List[ExpenseClaim])
async def get_expense_claims(
    skip: int = 0,
    limit: int = 20,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get list of expense claims for current user"""
    try:
        # Query expense claims from database
        query = """
        SELECT id, name, father_name, mother_name, created_by, created_at
        FROM accounts
        WHERE created_by = %(user_id)s
        ORDER BY created_at DESC
        LIMIT %(limit)s OFFSET %(skip)s
        """

        params = {
            "user_id": current_user.id,
            "limit": limit,
            "skip": skip
        }

        # For demo, return empty list
        # In real implementation, execute database query
        logger.info(f"Fetching expense claims for user {current_user.id}")

        return []

    except Exception as e:
        logger.error(f"Error fetching expense claims: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch expense claims"
        )

@app.get("/api/accounts/expense-claims/{claim_id}", response_model=ExpenseClaim)
async def get_expense_claim(
    claim_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get specific expense claim by ID"""
    try:
        # Query expense claim from database
        query = """
        SELECT id, name, father_name, mother_name, created_by, created_at
        FROM accounts
        WHERE id = %(claim_id)s AND created_by = %(user_id)s
        """

        params = {
            "claim_id": claim_id,
            "user_id": current_user.id
        }

        # For demo, raise not found
        # In real implementation, execute database query
        logger.info(f"Fetching expense claim {claim_id} for user {current_user.id}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense claim not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching expense claim {claim_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch expense claim"
        )

@app.delete("/api/accounts/expense-claims/{claim_id}")
async def delete_expense_claim(
    claim_id: int,
    current_user: UserInfo = Depends(get_current_user)
):
    """Delete expense claim"""
    try:
        # Check if expense claim exists and belongs to user
        query = """
        SELECT created_by FROM accounts
        WHERE id = %(claim_id)s
        """

        params = {"claim_id": claim_id}

        # For demo, return success response
        # In real implementation, execute database query and check ownership
        logger.info(f"Deleting expense claim {claim_id} for user {current_user.id}")

        return {
            "success": True,
            "message": "Expense claim deleted successfully"
        }

    except Exception as e:
        logger.error(f"Error deleting expense claim {claim_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete expense claim"
        )

@app.get("/api/accounts/reports/summary")
async def get_financial_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get financial summary report"""
    try:
        # Generate financial summary
        return {
            "total_income": 1000000.00,
            "total_expenses": 750000.00,
            "net_balance": 250000.00,
            "voucher_count": 150,
            "payment_count": 200,
            "period": {
                "start_date": start_date,
                "end_date": end_date
            }
        }

    except Exception as e:
        logger.error(f"Error generating financial summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate financial summary"
        )

@app.get("/api/accounts/reports/vouchers")
async def get_voucher_report(
    voucher_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """Get detailed voucher report"""
    try:
        # Generate voucher report
        return {
            "vouchers": [],
            "summary": {
                "total_vouchers": 0,
                "total_amount": 0.0,
                "by_type": {}
            },
            "filters": {
                "voucher_type": voucher_type,
                "start_date": start_date,
                "end_date": end_date
            }
        }

    except Exception as e:
        logger.error(f"Error generating voucher report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate voucher report"
        )

# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unexpected errors"""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
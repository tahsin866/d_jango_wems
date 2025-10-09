from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
import httpx
import os
from datetime import datetime
import uuid
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import aiofiles
import json

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/wifaq")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
PUBLICATION_UPLOAD_DIR = "/app/uploads"

# FastAPI App
app = FastAPI(title="Publication Service", version="1.0.0", description="Publication and Library Management Service")

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
os.makedirs(PUBLICATION_UPLOAD_DIR, exist_ok=True)

# Database Models
class Book(Base):
    __tablename__ = 'publication_books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    author = Column(String(255), nullable=False)
    author_bangla = Column(String(255))
    isbn = Column(String(20), unique=True, index=True)
    publisher = Column(String(255))
    publication_year = Column(Integer)
    edition = Column(String(50))
    language = Column(String(50))
    category = Column(String(100))
    subcategory = Column(String(100))
    marhala_id = Column(Integer)
    subject_id = Column(Integer)
    description = Column(Text)
    description_bangla = Column(Text)
    page_count = Column(Integer)
    price = Column(Numeric(10, 2))
    available_copies = Column(Integer, default=0)
    total_copies = Column(Integer, default=0)
    location = Column(String(100))
    file_path = Column(String(500))
    cover_image_path = Column(String(500))
    is_digital = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    madrasha_id = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Library(Base):
    __tablename__ = 'publication_libraries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_bangla = Column(String(255))
    description = Column(Text)
    description_bangla = Column(Text)
    location = Column(String(255))
    capacity = Column(Integer)
    operating_hours = Column(String(100))
    librarian_id = Column(Integer)
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    madrasha_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BookIssue(Base):
    __tablename__ = 'publication_book_issues'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('publication_books.id'), nullable=False)
    library_id = Column(Integer, ForeignKey('publication_libraries.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    status = Column(String(20), default='issued')  # issued, returned, overdue
    fine_amount = Column(Numeric(10, 2), default=0)
    notes = Column(Text)
    issued_by = Column(Integer)
    returned_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Journal(Base):
    __tablename__ = 'publication_journals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    issn = Column(String(20), unique=True, index=True)
    publisher = Column(String(255))
    frequency = Column(String(50))  # daily, weekly, monthly, quarterly, yearly
    volume = Column(Integer)
    issue = Column(Integer)
    publication_date = Column(Date)
    category = Column(String(100))
    language = Column(String(50))
    description = Column(Text)
    description_bangla = Column(Text)
    file_path = Column(String(500))
    cover_image_path = Column(String(500))
    is_digital = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    madrasha_id = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ResearchPaper(Base):
    __tablename__ = 'publication_research_papers'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    author = Column(String(255), nullable=False)
    author_bangla = Column(String(255))
    abstract = Column(Text)
    abstract_bangla = Column(Text)
    keywords = Column(String(500))
    publication_date = Column(Date)
    journal_id = Column(Integer, ForeignKey('publication_journals.id'))
    conference_name = Column(String(255))
    page_range = Column(String(50))
    doi = Column(String(100))
    url = Column(String(500))
    file_path = Column(String(500))
    category = Column(String(100))
    language = Column(String(50))
    is_published = Column(Boolean, default=False)
    peer_reviewed = Column(Boolean, default=False)
    madrasha_id = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Models
class BookBase(BaseModel):
    title: str
    title_bangla: Optional[str] = None
    author: str
    author_bangla: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    edition: Optional[str] = None
    language: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    marhala_id: Optional[int] = None
    subject_id: Optional[int] = None
    description: Optional[str] = None
    description_bangla: Optional[str] = None
    page_count: Optional[int] = None
    price: Optional[float] = None
    total_copies: Optional[int] = 0
    location: Optional[str] = None
    is_digital: bool = False
    madrasha_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    available_copies: int
    file_path: Optional[str] = None
    cover_image_path: Optional[str] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

class LibraryBase(BaseModel):
    name: str
    name_bangla: Optional[str] = None
    description: Optional[str] = None
    description_bangla: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    operating_hours: Optional[str] = None
    librarian_id: Optional[int] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    madrasha_id: int

class LibraryCreate(LibraryBase):
    pass

class LibraryResponse(LibraryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class BookIssueBase(BaseModel):
    book_id: int
    library_id: int
    user_id: int
    issue_date: str
    due_date: str
    notes: Optional[str] = None

class BookIssueCreate(BookIssueBase):
    pass

class BookIssueResponse(BookIssueBase):
    id: int
    return_date: Optional[str] = None
    status: str
    fine_amount: float
    issued_by: int
    returned_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class JournalBase(BaseModel):
    title: str
    title_bangla: Optional[str] = None
    issn: Optional[str] = None
    publisher: Optional[str] = None
    frequency: Optional[str] = None
    volume: Optional[int] = None
    issue: Optional[int] = None
    publication_date: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    description_bangla: Optional[str] = None
    is_digital: bool = False
    madrasha_id: int

class JournalCreate(JournalBase):
    pass

class JournalResponse(JournalBase):
    id: int
    file_path: Optional[str] = None
    cover_image_path: Optional[str] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

class ResearchPaperBase(BaseModel):
    title: str
    title_bangla: Optional[str] = None
    author: str
    author_bangla: Optional[str] = None
    abstract: Optional[str] = None
    abstract_bangla: Optional[str] = None
    keywords: Optional[str] = None
    publication_date: Optional[str] = None
    journal_id: Optional[int] = None
    conference_name: Optional[str] = None
    page_range: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    is_published: bool = False
    peer_reviewed: bool = False
    madrasha_id: int

class ResearchPaperCreate(ResearchPaperBase):
    pass

class ResearchPaperResponse(ResearchPaperBase):
    id: int
    file_path: Optional[str] = None
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

# Books Endpoints
@app.post("/books", response_model=BookResponse)
async def create_book(
    book: BookCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin", "librarian"]:
        raise HTTPException(status_code=403, detail="Not authorized to create books")

    db_book = Book(**book.dict(), created_by=current_user["id"])
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@app.get("/books", response_model=List[BookResponse])
async def get_books(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    language: Optional[str] = None,
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Book).where(Book.is_active == True)

    if madrasha_id or current_user.get("role") == "madrasha":
        query = query.where(Book.madrasha_id == (madrasha_id or current_user.get("madrasha_id")))

    if category:
        query = query.where(Book.category == category)
    if language:
        query = query.where(Book.language == language)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Book).where(Book.id == book_id, Book.is_active == True)
    result = await db.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.post("/books/{book_id}/upload")
async def upload_book_file(
    book_id: int,
    file: UploadFile = File(...),
    cover_image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin", "librarian"]:
        raise HTTPException(status_code=403, detail="Not authorized to upload files")

    query = select(Book).where(Book.id == book_id)
    result = await db.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if file:
        file_path = await save_upload_file(file, PUBLICATION_UPLOAD_DIR)
        book.file_path = file_path

    if cover_image:
        cover_path = await save_upload_file(cover_image, PUBLICATION_UPLOAD_DIR)
        book.cover_image_path = cover_path

    await db.commit()
    return {"message": "Files uploaded successfully", "file_path": file_path}

# Library Endpoints
@app.post("/libraries", response_model=LibraryResponse)
async def create_library(
    library: LibraryCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create libraries")

    db_library = Library(**library.dict())
    db.add(db_library)
    await db.commit()
    await db.refresh(db_library)
    return db_library

@app.get("/libraries", response_model=List[LibraryResponse])
async def get_libraries(
    skip: int = 0,
    limit: int = 100,
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Library).where(Library.is_active == True)

    if madrasha_id or current_user.get("role") == "madrasha":
        query = query.where(Library.madrasha_id == (madrasha_id or current_user.get("madrasha_id")))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Book Issue Endpoints
@app.post("/issues", response_model=BookIssueResponse)
async def issue_book(
    issue: BookIssueCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin", "librarian"]:
        raise HTTPException(status_code=403, detail="Not authorized to issue books")

    # Check book availability
    book_query = select(Book).where(Book.id == issue.book_id, Book.is_active == True)
    book_result = await db.execute(book_query)
    book = book_result.scalar_one_or_none()

    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    # Create book issue
    db_issue = BookIssue(**issue.dict(), issued_by=current_user["id"])
    db.add(db_issue)

    # Update available copies
    book.available_copies -= 1

    await db.commit()
    await db.refresh(db_issue)
    return db_issue

@app.post("/issues/{issue_id}/return")
async def return_book(
    issue_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin", "librarian"]:
        raise HTTPException(status_code=403, detail="Not authorized to return books")

    query = select(BookIssue).where(BookIssue.id == issue_id, BookIssue.status == 'issued')
    result = await db.execute(query)
    issue = result.scalar_one_or_none()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found or already returned")

    # Update issue
    issue.status = 'returned'
    issue.return_date = datetime.now().date()
    issue.returned_by = current_user["id"]

    # Update book availability
    book_query = select(Book).where(Book.id == issue.book_id)
    book_result = await db.execute(book_query)
    book = book_result.scalar_one()
    book.available_copies += 1

    await db.commit()
    return {"message": "Book returned successfully"}

@app.get("/issues", response_model=List[BookIssueResponse])
async def get_book_issues(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(BookIssue)

    if status:
        query = query.where(BookIssue.status == status)
    if user_id:
        query = query.where(BookIssue.user_id == user_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Journal Endpoints
@app.post("/journals", response_model=JournalResponse)
async def create_journal(
    journal: JournalCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin", "librarian"]:
        raise HTTPException(status_code=403, detail="Not authorized to create journals")

    db_journal = Journal(**journal.dict(), created_by=current_user["id"])
    db.add(db_journal)
    await db.commit()
    await db.refresh(db_journal)
    return db_journal

@app.get("/journals", response_model=List[JournalResponse])
async def get_journals(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Journal).where(Journal.is_active == True)

    if madrasha_id or current_user.get("role") == "madrasha":
        query = query.where(Journal.madrasha_id == (madrasha_id or current_user.get("madrasha_id")))

    if category:
        query = query.where(Journal.category == category)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Research Paper Endpoints
@app.post("/research-papers", response_model=ResearchPaperResponse)
async def create_research_paper(
    paper: ResearchPaperCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") not in ["master_admin", "admin", "teacher", "researcher"]:
        raise HTTPException(status_code=403, detail="Not authorized to create research papers")

    db_paper = ResearchPaper(**paper.dict(), created_by=current_user["id"])
    db.add(db_paper)
    await db.commit()
    await db.refresh(db_paper)
    return db_paper

@app.get("/research-papers", response_model=List[ResearchPaperResponse])
async def get_research_papers(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    is_published: Optional[bool] = None,
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(ResearchPaper)

    if madrasha_id or current_user.get("role") == "madrasha":
        query = query.where(ResearchPaper.madrasha_id == (madrasha_id or current_user.get("madrasha_id")))

    if category:
        query = query.where(ResearchPaper.category == category)
    if is_published is not None:
        query = query.where(ResearchPaper.is_published == is_published)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Statistics Endpoints
@app.get("/statistics")
async def get_publication_statistics(
    madrasha_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if madrasha_id or current_user.get("role") == "madrasha":
        madrasha_id = madrasha_id or current_user.get("madrasha_id")

    # Count books
    books_query = select(Book).where(Book.madrasha_id == madrasha_id, Book.is_active == True)
    books_result = await db.execute(books_query)
    total_books = len(books_result.scalars().all())

    # Count active issues
    issues_query = select(BookIssue).join(Book).where(
        Book.madrasha_id == madrasha_id,
        BookIssue.status == 'issued'
    )
    issues_result = await db.execute(issues_query)
    active_issues = len(issues_result.scalars().all())

    # Count journals
    journals_query = select(Journal).where(Journal.madrasha_id == madrasha_id, Journal.is_active == True)
    journals_result = await db.execute(journals_query)
    total_journals = len(journals_result.scalars().all())

    # Count research papers
    papers_query = select(ResearchPaper).where(ResearchPaper.madrasha_id == madrasha_id)
    papers_result = await db.execute(papers_query)
    total_papers = len(papers_result.scalars().all())

    return {
        "total_books": total_books,
        "active_issues": active_issues,
        "total_journals": total_journals,
        "total_research_papers": total_papers
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "publication-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
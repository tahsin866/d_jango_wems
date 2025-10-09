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

# FastAPI App
app = FastAPI(title="Administration Service", version="1.0.0", description="System Administration and User Management Service")

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

# Enums
class UserRole(PyEnum):
    master_admin = "master_admin"
    super_admin = "super_admin"
    board_admin = "board_admin"
    admin = "admin"
    teacher = "teacher"
    student = "student"
    parent = "parent"
    staff = "staff"

class ActivityLogType(PyEnum):
    login = "login"
    logout = "logout"
    create = "create"
    update = "update"
    delete = "delete"
    view = "view"
    export = "export"
    import_ = "import"
    print = "print"
    approve = "approve"
    reject = "reject"

# Database Models
class SystemSettings(Base):
    __tablename__ = 'admin_system_settings'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(Text)
    description = Column(Text)
    data_type = Column(String(50), default='string')  # string, number, boolean, json
    category = Column(String(100))
    is_public = Column(Boolean, default=False)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserActivity(Base):
    __tablename__ = 'admin_user_activity'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_role = Column(String(50))
    action_type = Column(Enum(ActivityLogType))
    resource_type = Column(String(100))
    resource_id = Column(Integer)
    details = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    status_code = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class UserSession(Base):
    __tablename__ = 'admin_user_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    session_token = Column(String(500), unique=True, index=True)
    refresh_token = Column(String(500), unique=True)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)

class SystemAnnouncement(Base):
    __tablename__ = 'admin_system_announcements'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_bangla = Column(String(255))
    content = Column(Text, nullable=False)
    content_bangla = Column(Text)
    announcement_type = Column(String(50))  # info, warning, maintenance, holiday
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    target_roles = Column(Text)  # JSON array of roles
    target_madrashas = Column(Text)  # JSON array of madrasha IDs
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserPermission(Base):
    __tablename__ = 'admin_user_permissions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    permission = Column(String(255), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(Integer)
    granted_by = Column(Integer)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

class BackupLog(Base):
    __tablename__ = 'admin_backup_logs'

    id = Column(Integer, primary_key=True, index=True)
    backup_type = Column(String(50))  # full, incremental, differential
    database_name = Column(String(100))
    file_path = Column(String(500))
    file_size = Column(Integer)
    status = Column(String(20))  # started, completed, failed
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class SystemSettingsBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    data_type: str = 'string'
    category: Optional[str] = None
    is_public: bool = False

class SystemSettingsCreate(SystemSettingsBase):
    pass

class SystemSettingsUpdate(BaseModel):
    value: str
    description: Optional[str] = None

class SystemSettingsResponse(SystemSettingsBase):
    id: int
    updated_by: Optional[int] = None
    updated_at: datetime
    created_at: datetime

class UserActivityResponse(BaseModel):
    id: int
    user_id: int
    user_role: Optional[str] = None
    action_type: ActivityLogType
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status_code: Optional[int] = None
    created_at: datetime

class SystemAnnouncementBase(BaseModel):
    title: str
    title_bangla: Optional[str] = None
    content: str
    content_bangla: Optional[str] = None
    announcement_type: str = 'info'
    priority: str = 'normal'
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    target_roles: Optional[List[str]] = None
    target_madrashas: Optional[List[int]] = None

class SystemAnnouncementCreate(SystemAnnouncementBase):
    pass

class SystemAnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    title_bangla: Optional[str] = None
    content: Optional[str] = None
    content_bangla: Optional[str] = None
    announcement_type: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    target_roles: Optional[List[str]] = None
    target_madrashas: Optional[List[int]] = None
    is_active: Optional[bool] = None

class SystemAnnouncementResponse(SystemAnnouncementBase):
    id: int
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class UserPermissionBase(BaseModel):
    user_id: int
    permission: str
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    expires_at: Optional[str] = None

class UserPermissionCreate(UserPermissionBase):
    pass

class UserPermissionResponse(UserPermissionBase):
    id: int
    granted_by: Optional[int] = None
    granted_at: datetime
    is_active: bool

class BackupLogResponse(BaseModel):
    id: int
    backup_type: str
    database_name: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime

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

# Activity Logging
async def log_user_activity(
    db: AsyncSession,
    user_id: int,
    user_role: str,
    action_type: ActivityLogType,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status_code: Optional[int] = None
):
    activity = UserActivity(
        user_id=user_id,
        user_role=user_role,
        action_type=action_type,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        status_code=status_code
    )
    db.add(activity)
    await db.commit()

# System Settings Endpoints
@app.post("/settings", response_model=SystemSettingsResponse)
async def create_setting(
    setting: SystemSettingsCreate,
    request,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if setting already exists
    existing_query = select(SystemSettings).where(SystemSettings.key == setting.key)
    existing_result = await db.execute(existing_query)
    if existing_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Setting key already exists")

    db_setting = SystemSettings(**setting.dict(), updated_by=current_user["id"])
    db.add(db_setting)
    await db.commit()
    await db.refresh(db_setting)

    await log_user_activity(
        db, current_user["id"], current_user["role"],
        ActivityLogType.create, "system_setting", db_setting.id,
        f"Created setting: {setting.key}"
    )

    return db_setting

@app.get("/settings", response_model=List[SystemSettingsResponse])
async def get_settings(
    category: Optional[str] = None,
    is_public: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SystemSettings)

    if category:
        query = query.where(SystemSettings.category == category)
    if is_public is not None:
        query = query.where(SystemSettings.is_public == is_public)

    result = await db.execute(query)
    return result.scalars().all()

@app.get("/settings/{setting_id}", response_model=SystemSettingsResponse)
async def get_setting(
    setting_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SystemSettings).where(SystemSettings.id == setting_id)
    result = await db.execute(query)
    setting = result.scalar_one_or_none()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    return setting

@app.put("/settings/{setting_id}", response_model=SystemSettingsResponse)
async def update_setting(
    setting_id: int,
    setting_update: SystemSettingsUpdate,
    request,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SystemSettings).where(SystemSettings.id == setting_id)
    result = await db.execute(query)
    setting = result.scalar_one_or_none()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    for field, value in setting_update.dict(exclude_unset=True).items():
        setattr(setting, field, value)

    setting.updated_by = current_user["id"]
    await db.commit()
    await db.refresh(setting)

    await log_user_activity(
        db, current_user["id"], current_user["role"],
        ActivityLogType.update, "system_setting", setting_id,
        f"Updated setting: {setting.key}"
    )

    return setting

# Activity Log Endpoints
@app.get("/activity", response_model=List[UserActivityResponse])
async def get_activity_logs(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    action_type: Optional[ActivityLogType] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserActivity)

    if user_id:
        query = query.where(UserActivity.user_id == user_id)
    if action_type:
        query = query.where(UserActivity.action_type == action_type)
    if start_date:
        query = query.where(UserActivity.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.where(UserActivity.created_at <= datetime.fromisoformat(end_date))

    query = query.order_by(UserActivity.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Announcement Endpoints
@app.post("/announcements", response_model=SystemAnnouncementResponse)
async def create_announcement(
    announcement: SystemAnnouncementCreate,
    request,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    data = announcement.dict()
    if data.get("target_roles"):
        data["target_roles"] = json.dumps(data["target_roles"])
    if data.get("target_madrashas"):
        data["target_madrashas"] = json.dumps(data["target_madrashas"])

    db_announcement = SystemAnnouncement(**data, created_by=current_user["id"])
    db.add(db_announcement)
    await db.commit()
    await db.refresh(db_announcement)

    await log_user_activity(
        db, current_user["id"], current_user["role"],
        ActivityLogType.create, "announcement", db_announcement.id,
        f"Created announcement: {announcement.title}"
    )

    return db_announcement

@app.get("/announcements", response_model=List[SystemAnnouncementResponse])
async def get_announcements(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SystemAnnouncement)

    if is_active is not None:
        query = query.where(SystemAnnouncement.is_active == is_active)

    query = query.order_by(SystemAnnouncement.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    announcements = result.scalars().all()

    # Parse JSON fields
    for announcement in announcements:
        if announcement.target_roles:
            announcement.target_roles = json.loads(announcement.target_roles)
        if announcement.target_madrashas:
            announcement.target_madrashas = json.loads(announcement.target_madrashas)

    return announcements

@app.put("/announcements/{announcement_id}", response_model=SystemAnnouncementResponse)
async def update_announcement(
    announcement_id: int,
    announcement_update: SystemAnnouncementUpdate,
    request,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SystemAnnouncement).where(SystemAnnouncement.id == announcement_id)
    result = await db.execute(query)
    announcement = result.scalar_one_or_none()

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    update_data = announcement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field in ["target_roles", "target_madrashas"] and value is not None:
            setattr(announcement, field, json.dumps(value))
        else:
            setattr(announcement, field, value)

    await db.commit()
    await db.refresh(announcement)

    await log_user_activity(
        db, current_user["id"], current_user["role"],
        ActivityLogType.update, "announcement", announcement_id,
        f"Updated announcement: {announcement.title}"
    )

    # Parse JSON fields for response
    if announcement.target_roles:
        announcement.target_roles = json.loads(announcement.target_roles)
    if announcement.target_madrashas:
        announcement.target_madrashas = json.loads(announcement.target_madrashas)

    return announcement

# User Permission Endpoints
@app.post("/permissions", response_model=UserPermissionResponse)
async def grant_permission(
    permission: UserPermissionCreate,
    request,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_permission = UserPermission(**permission.dict(), granted_by=current_user["id"])
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)

    await log_user_activity(
        db, current_user["id"], current_user["role"],
        ActivityLogType.create, "user_permission", db_permission.id,
        f"Granted permission: {permission.permission} to user {permission.user_id}"
    )

    return db_permission

@app.get("/permissions", response_model=List[UserPermissionResponse])
async def get_user_permissions(
    user_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserPermission).where(UserPermission.is_active == True)

    if user_id:
        query = query.where(UserPermission.user_id == user_id)

    result = await db.execute(query)
    return result.scalars().all()

@app.delete("/permissions/{permission_id}")
async def revoke_permission(
    permission_id: int,
    request,
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserPermission).where(UserPermission.id == permission_id)
    result = await db.execute(query)
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    permission.is_active = False
    await db.commit()

    await log_user_activity(
        db, current_user["id"], current_user["role"],
        ActivityLogType.delete, "user_permission", permission_id,
        f"Revoked permission: {permission.permission} from user {permission.user_id}"
    )

    return {"message": "Permission revoked successfully"}

# Statistics Endpoints
@app.get("/statistics")
async def get_admin_statistics(
    current_user: dict = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Count active users
    active_sessions_query = select(UserSession).where(UserSession.is_active == True)
    active_sessions_result = await db.execute(active_sessions_query)
    active_users = len(active_sessions_result.scalars().all())

    # Count today's activities
    today = datetime.now().date()
    today_activities_query = select(UserActivity).where(
        UserActivity.created_at >= today
    )
    today_activities_result = await db.execute(today_activities_query)
    today_activities = len(today_activities_result.scalars().all())

    # Count active announcements
    active_announcements_query = select(SystemAnnouncement).where(
        SystemAnnouncement.is_active == True
    )
    active_announcements_result = await db.execute(active_announcements_query)
    active_announcements = len(active_announcements_result.scalars().all())

    # Count user permissions
    active_permissions_query = select(UserPermission).where(
        UserPermission.is_active == True
    )
    active_permissions_result = await db.execute(active_permissions_query)
    active_permissions = len(active_permissions_result.scalars().all())

    return {
        "active_users": active_users,
        "today_activities": today_activities,
        "active_announcements": active_announcements,
        "active_permissions": active_permissions
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "administration-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Web-based Education Management System (WEMS)** for Islamic educational institutions (madrashas) in Bangladesh. It's a full-stack application with Django REST API backend and Vue.js frontend.

## Development Commands

### Backend (Django)
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Collect static files
python manage.py collectstatic
```

### Frontend (Vue.js)
```bash
cd wems-frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format
```

## Architecture Overview

### Backend Structure
- **Django 5.2.5** with REST Framework
- **PostgreSQL** database named 'wifaq'
- **Custom authentication** supporting email/phone login
- **Role-based access control** with multiple user types
- **Mixed managed/unmanaged models** for existing database integration

### Key Django Apps
1. **`users`** - Custom user management with role-based permissions
2. **`school`** - Madrasha/school management (unmanaged models)
3. **`subject`** - Curriculum management with multi-language support
4. **`CentralExam`** - Exam coordination and fee management
5. **`Markaz`** - Educational center applications and document processing
6. **`admin.registration.*`** - Registration management and statistics

### Frontend Structure
- **Vue 3** with Composition API and TypeScript
- **TailAdmin** template as base UI framework
- **PrimeVue** components library
- **Tailwind CSS** for styling
- **Vite** as build tool

### Authentication & Security
- Custom `EmailOrPhoneBackend` authentication
- JWT middleware with role-based route protection
- Session management with Redis/memory cache fallback
- CORS configuration for frontend integration

### Database Patterns
- Uses both managed and unmanaged Django models
- Unmanaged models connect to existing database tables
- Proper indexing and relationship management
- Native language field names (Bengali, English, Arabic)

## API Structure
- `/auth/` - Authentication endpoints
- `/api/central-exam/` - Exam management
- `/api/markaz/` - Center applications
- `/api/admin/registration/` - Registration management
- `/api/sidebar/` - Navigation and menu data

## Development Notes

### User Roles
- Master Admin, Super Admin, Board Admin, Admin
- Layout-based access control enforced by middleware
- Role-specific routing and permissions

### Multi-language Support
- Bengali, English, and Arabic language support
- Culturally adapted for Bangladeshi educational context

### Security Considerations
- Activity logging and audit trails
- Session-based security with JWT tokens
- bcrypt fallback for password hashing
- CORS and CSRF protection configured

### Frontend Development
- Development server runs on localhost:5173
- Uses Vite for fast development and building
- TypeScript for type safety
- ESLint and Prettier configured for code quality
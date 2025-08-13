# Хром-КЗ Logistics Management System

## Overview

Внутренняя система управления логистикой для департамента логистики компании "Хром-КЗ". Система автоматизирует управление заказами и отслеживание грузоперевозок по Астане и по всему Казахстану. Приложение включает публичный интерфейс для клиентов для подачи заказов и отслеживания отправлений, а также административную панель для сотрудников для управления заказами, назначения водителей и создания отчетов.

This is an internal corporate product specifically designed for Chrome-KZ company's logistics department. The system supports two types of deliveries: local Astana deliveries and nationwide Kazakhstan shipments. It includes role-based access control, automated notifications via Telegram, and comprehensive analytics for business insights.

## User Preferences

Preferred communication style: Simple, everyday language.
UI/UX Design: Modern design patterns with contemporary colors, enhanced animations, dark theme support, improved typography using Inter font family, glassmorphism effects, and enhanced user interactions.
Admin Panel Layout: Left sidebar navigation menu (requested 2025-08-13) - menu should be integrated as a true sidebar on the left side, not below content, to match system identity.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
- **Styling**: Custom CSS with Font Awesome icons and modern, minimalist white-based design
- **Client-side**: Vanilla JavaScript for form validation, phone formatting, and interactive features
- **Charts**: Chart.js for analytics visualization

### Backend Architecture
- **Framework**: Flask web framework with modular structure
- **Authentication**: Flask-Login for session management with role-based access control
- **Forms**: Flask-WTF for secure form handling and CSRF protection
- **Database ORM**: SQLAlchemy with declarative base for database operations
- **Middleware**: ProxyFix for handling reverse proxy headers

### Data Model
- **Users**: Employee and logist roles with authentication and profile management
- **Orders**: Comprehensive order tracking with status management, customer info, and shipping details
- **Drivers**: Driver management with vehicle information and assignment tracking
- **Relationships**: Foreign key relationships between users, orders, and drivers

### Security Features
- **Session Management**: Secure session handling with configurable secret keys
- **Form Validation**: Server-side validation with WTForms
- **CSRF Protection**: Built-in CSRF token validation
- **Password Hashing**: Werkzeug security for password management

### Business Logic
- **Order Workflow**: Multi-status order lifecycle (new, confirmed, in_progress, delivered, cancelled)
- **Role-based Access**: Different permissions for employees vs logists
- **Tracking System**: Unique tracking number generation and customer tracking interface
- **Notification System**: Automated notifications for order updates

## External Dependencies

### Database
- **SQLite**: Primary database with fallback to local file storage
- **PostgreSQL**: Configurable via DATABASE_URL environment variable
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

### Messaging Services
- **Telegram Bot API**: Integration for automated order notifications to logistics team
- **SMS Service**: Placeholder integration for customer SMS notifications (SMS.ru, SMSC.ru compatible)

### Third-party Libraries
- **Bootstrap 5**: Frontend CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **Chart.js**: JavaScript charting library for analytics dashboards

### Environment Configuration
- **SESSION_SECRET**: Configurable session encryption key
- **DATABASE_URL**: Database connection string (supports SQLite and PostgreSQL)
- **TELEGRAM_BOT_TOKEN**: Bot token for Telegram notifications
- **TELEGRAM_CHAT_ID**: Target chat/channel for notifications

### Deployment Considerations
- **WSGI**: Flask WSGI application with ProxyFix middleware
- **Static Assets**: CDN-hosted Bootstrap, Font Awesome, and Chart.js
- **File Structure**: Modular organization with separate routes, models, forms, and utilities
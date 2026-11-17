# Multi-Vendor E-Commerce Platform

## Project Overview
A Multi-Vendor E-Commerce Platform built using React, FastAPI, and MySQL. It supports Admin, Vendor, and Customer roles with JWT-based authentication and role-based access control.

## Technologies Used

### Frontend
- React.js
- Vite
- Axios
- React Router DOM

### Backend
- Python
- FastAPI
- SQLAlchemy
- JWT Authentication
- Argon2 Password Hashing

### Database
- MySQL

## Project Structure

```text
multi_vendor_ecommerce/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
│
├── auth_service/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── dependencies/
│   │   └── utils/
│   ├── .env
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

## User Roles

- Admin
- Vendor
- Customer

## Authentication Features

- User Registration
- User Login
- JWT Access Token
- JWT Refresh Token
- User Logout
- Password Hashing
- Protected Routes
- Role-Based Access Control
- User Management
- Account Activation and Deactivation

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | User registration |
| POST | /auth/login | User login |
| GET | /auth/me | Current user |
| POST | /auth/refresh | Refresh token |
| POST | /auth/logout | User logout |
| GET | /users/ | List users (Admin) |
| GET | /users/{id} | Get user |
| PUT | /users/{id} | Update user |
| PATCH | /users/{id}/status | Update user status |
| PATCH | /users/{id}/role | Update user role |

## How to Run

### Backend

```bash
cd auth_service
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Swagger documentation:

http://127.0.0.1:8001/docs

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

http://localhost:5173/

## Database

Create a MySQL database named:

`auth_db`

Configure the database connection and JWT secret in `auth_service/.env`.

## Testing

The following tests were completed:

- Vendor Registration
- Customer Registration
- Admin Login
- Vendor Login
- Customer Login
- JWT Authentication
- User Management APIs
- Role-Based Navigation
- Customer Dashboard
- Vendor Dashboard
- Admin Dashboard

## Project Status

Day 1 – Authentication Service and Frontend Integration Completed.
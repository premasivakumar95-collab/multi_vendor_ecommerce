from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import User, RefreshToken
from app.routes import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Multi-Vendor E-Commerce Authentication API",
    description="Authentication, JWT, RBAC and User Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Multi-Vendor E-Commerce Auth Service Running"}


@app.get("/health")
def health():
    return {"status": "ok"}

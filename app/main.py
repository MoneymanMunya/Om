from schemas import UserSchema
from database import get_db

from fastapi import FastAPI

app = FastAPI()

@app.get("/user")
def home():
    return {"message": "FastAPI is working!"}

@app.post("/users")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    ...
app.include_router(users_router, prefix="/users", tags=["Users"])
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas
from routes.users import users_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create a new user (POST /users)
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

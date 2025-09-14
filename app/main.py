from fastapi import FastAPI
from .database import engine, Base
from .routes.user import router as user_router
from .routes.tasks import router as tasks_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Omni API",
    description="API for the Omni personal AI companion app.",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to Omni API!"}

# Include router
# There is a typo in the original `main.py`: `users_router` should be `user_router`
# and it should be imported from `.routes.user`, not `routes.users`
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

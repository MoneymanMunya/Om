from fastapi import FastAPI

app = FastAPI()

@app.get("/user")
def home():
    return {"message": "FastAPI is working!"}

@app.post("/users")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    ...
app.include_router(users_router, prefix="/users", tags=["Users"])

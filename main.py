from fastapi import FastAPI
from routers import users, tasks, rewards, ai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/users", tags=["Users"])
@app.get("/")
async def root():
    return {"message": "Welcome to our MiniApp API!"}
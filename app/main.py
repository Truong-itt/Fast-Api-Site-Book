from fastapi import FastAPI
from . import models
from .database import engine
# from .routers import reviews, books, users, categories
from app.routers import router 
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Truongitt API", version="0.1.0")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["home"])
async def read_root():
    return {"message": "Welcome to Truongitt Listening API"}

@app.get("/db_health", tags=["home"])
async def database_connection():
    db = engine.connect()
    if db:
        return {"message": "Database connection is ok."}
    else:
        return {"message": "Database connection is Fail."}
    
app.include_router(router)
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import (
    engine,
    create_db_and_tables,
    insert_users,
    insert_plan,
    insert_wiki_information,
    insert_symbol_dictionary,
)
from models import *
from sqlmodel import Session
from domain.account import account_router
from domain.post import post_router
from domain.draft import draft_router
from domain.user import user_router
from domain.data import data_router
from domain.reply import reply_router
from domain.search import search_router
from domain.others import others_router
from domain.admin import admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define what to do on startup and termination of the application"""
    # [1] The first part of the function　will be executed before the backend server starts

    # Check whether db and table already exist or not
    # This prevents Google Cloud SQL from losing all data, overwriting tables and all risks
    try:
        with Session(engine) as session:
            user = session.get(Users, 1)
    except:
        print("Creating database and tables...")
        create_db_and_tables()

    # The below code is just for development and test: checking whether data exist already or not
    with Session(engine) as session:

        # Plan
        plan = session.get(Plan, 1)
        if not plan:
            insert_plan()
        
        # Users
        user = session.get(Users, 1)
        if not user:
            insert_users()

        # Wiki Information
        if not session.get(Wiki, 1):
            insert_wiki_information()

        # Symbol Index Yahoo
        if not session.get(SymbolDictionary, 1):
            insert_symbol_dictionary()

    yield
    # [2] The part after the yield will be executed after the backend server has terminated


app = FastAPI(
    lifespan=lifespan,
    # [DEV or PROD] For development, please comment out the next two arguments
    docs_url=None,
    redoc_url=None,
)

app.include_router(account_router.router)
app.include_router(post_router.router)
app.include_router(draft_router.router)
app.include_router(user_router.router)
app.include_router(reply_router.router)
app.include_router(data_router.router)
app.include_router(search_router.router)
app.include_router(others_router.router)
app.include_router(admin_router.router)

app.mount("/assets", StaticFiles(directory="./frontend/dist/assets"))

origins = [
    "http://localhost:5173",    
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:5173",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return FileResponse("./frontend/dist/assets/index.html")

if __name__ == "__main__":
    # Don't forget to set host 0.0.0.0
    # Because the pgm does not work in a Docker container environment!
    # [DEV or PROD] reload should be False if PROD
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
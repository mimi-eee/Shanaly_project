from sqlmodel import create_engine, SQLModel, Session
from models import *
import os
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy

import pandas as pd
from datetime import datetime as dt
from passlib.context import CryptContext

# [PARAMETER]
SALT = os.getenv("SALT")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# --------- [PROD] Google Cloud SQL --------- #
if os.getenv("ENV_PROD") == "YES":
    # https://cloud.google.com/sql/docs/postgres/connect-run

    # [PARAMETER]
    PROJECT_ID = os.getenv("PROJECT_ID")
    REGION = os.getenv("REGION")
    DB_INSTANCE_ID = os.getenv("DB_INSTANCE_ID")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    DRIVER = os.getenv("DRIVER")

    def connect_with_connector():
        # Set ip_type
        ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") else IPTypes.PUBLIC

        # initialize Cloud SQL Python Connector object
        connector = Connector()

        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                f"{PROJECT_ID}:{REGION}:{DB_INSTANCE_ID}", # jspark-dev:asia-northeast1:jspark-testdb-postgres
                DRIVER,
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME,
                ip_type=ip_type,
            )
            return conn

        pool = sqlalchemy.create_engine(
            f"postgresql+{DRIVER}://",
            creator=getconn,
            echo=False,
        )
        return pool

    # Create an engine
    engine = connect_with_connector()

# --------- [DEV] PostgreSQL by Docker image --------- #
else:
    # https://hub.docker.com/_/postgres
    # Tag = 16.2-alpine3.19

    # Parameters
    POSTGRESQL_LOCAL_URL = os.getenv("POSTGRESQL_LOCAL_URL")

    # Create an engine
    engine = create_engine(POSTGRESQL_LOCAL_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

#----------- Insert Basic Data-----------------#

def insert_users():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    with Session(engine) as session:
        # Admin User
        user_admin = Users(
            email="admin@shanaly.com",
            username="admin",
            password=pwd_context.hash(ADMIN_PASSWORD + SALT),
            status_msg="ADMIN USER",
            is_verified=True,
            is_admin=True,
            created_at=dt.now(),
            plan_id=2, # Advanced Plan
        )
        session.add(user_admin)
        session.commit()

def insert_plan():
    with Session(engine) as session:
        # Plan ID = 1
        plan_1 = Plan(
            plan_name_jpn="無料",
            plan_name_eng="Free",
        )
        # Plan ID = 2
        plan_2 = Plan(
            plan_name_jpn="アドバンスト",
            plan_name_eng="Advanced",
        )
        session.add(plan_1)
        session.add(plan_2)
        session.commit()

def insert_wiki_information():
    data_dict = (
        pd
        .read_csv("./init_data/financial_terms.csv")
        .astype({"ready": bool})
        .to_dict('records')
    )

    with Session(engine) as session:
        session.bulk_insert_mappings(Wiki, data_dict)
        session.commit()


def insert_symbol_dictionary():
    data_dict = (
        pd
        .read_csv("./init_data/symbols_names_index.csv")
        .to_dict('records')
    )

    with Session(engine) as session:
        session.bulk_insert_mappings(SymbolDictionary, data_dict)
        session.commit()
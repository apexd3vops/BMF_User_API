from typing import List, Optional
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi import FastAPI, Depends
from . import models
from app.db import setting, engine
from .routers import users, auth



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

while True:
    try: 
        conn = psycopg2.connect(host= f'{setting.DATABASE_HOSTNAME}', database = f'{setting.DATABASE_NAME}', user=f'{setting.DATABASE_USERNAME}', password= f'{setting.DATABASE_PASSWORD}', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Succesfull Database Handshake")
        break
    except Exception as error:
        print("Database Handshake Failed")
        print("Error: ", error)
        time.sleep(10)

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}



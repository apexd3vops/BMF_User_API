from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from app.db import setting
import time

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/oauth")
def login_user():
    return {"User": "Successfully logged in"}

@app.post("/signup")
def create_users():
    return {"User": "created successfully"}

@app.put("/users")
def update_users():
    return {"User": "Successfully Updated"}

@app.get("/users")
def get_users():
    return {"User": "All users in db"}

@app.delete("/user")
def delete_users():
    return {"User": "Deleted Successfully"}

@app.get("/users/{id}")
def get_user():
    return {"User": f"All user in db with the id {id}"}
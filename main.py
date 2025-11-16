from fastapi import FastAPI, HTTPException, Query
from models import User, Category, Record
from data import users, categories, records
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import datetime

app = FastAPI(title="Expense Tracker API")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": 500, "error": str(exc)}
    )

@app.post("/users/", response_model=User)
def create_user(user: User):
    new_id = len(users) + 1
    new_user = User(id=new_id, name=user.name)
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(404, "User not found")

@app.get("/users")
def list_users():
    return users

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"detail": "User deleted"}
    raise HTTPException(404, "User not found")

@app.post("/categories/", response_model=Category)
def create_category(category: Category):
    new_id = len(categories) + 1
    new_cat = Category(id=new_id, title=category.title)
    categories.append(new_cat)
    return new_cat

@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int):
    for category in categories:
        if category.id == category_id:
            return category
    raise HTTPException(404, "Category not found")

@app.get("/categories")
def list_categories():
    return categories

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return {"detail": "Category deleted"}
    raise HTTPException(404, "Category not found")

@app.post("/records/", response_model=Record)
def create_record(record: Record):

    
    if not any(u.id == record.user_id for u in users):
        raise HTTPException(400, "User does not exist")

    if not any(c.id == record.category_id for c in categories):
        raise HTTPException(400, "Category does not exist")

    new_id = len(records) + 1
    new_record = Record(
        id=new_id,
        user_id=record.user_id,
        category_id=record.category_id,
        amount=record.amount,
        timestamp=record.timestamp
    )
    records.append(new_record)
    return new_record

@app.get("/records/{record_id}", response_model=Record)
def get_record(record_id: int):
    for record in records:
        if record.id == record_id:
            return record
    raise HTTPException(404, "Record not found")

@app.get("/records")
def list_records(user_id: int = Query(None), category_id: int = Query(None)):
    filtered = records
    if user_id is not None:
        filtered = [record for record in filtered if record.user_id == user_id]
    if category_id is not None:
        filtered = [record for record in filtered if record.category_id == category_id]
    return filtered

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    for record in records:
        if record.id == record_id:
            records.remove(record)
            return {"detail": "Record deleted"}
    raise HTTPException(404, "Record not found")


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
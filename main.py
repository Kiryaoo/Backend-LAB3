from fastapi import FastAPI, HTTPException, Query
from models import User, Category, Record
from data import users, categories, records
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code},
    )

app = FastAPI(title="Expense Tracker API")

@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int): 
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users")
def list_users():
    return users

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/categories/", response_model=Category)
def create_category(category: Category):
    categories.append(category)
    return category

@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int):
    for category in categories:
        if category.id == category_id:
            return category
    raise HTTPException(status_code=404, detail="Category not found")

@app.get("/categories")
def list_categories():
    return categories

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return {"detail": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")

@app.post("/records/", response_model=Record)
def create_record(record: Record):      
    records.append(record)
    return record                       

@app.get("/records/{record_id}", response_model=Record)                 
def get_record(record_id: int):         
    for record in records:              
        if record.id == record_id:      
            return record               
    raise HTTPException(status_code=404, detail="Record not found")
    
@app.get("/records")
def list_records(user_id: int = Query(None), category_id: int = Query(None)):
    filtered_records = records
    if user_id is not None:
        filtered_records = [r for r in filtered_records if r.user_id == user_id]
    if category_id is not None:
        filtered_records = [r for r in filtered_records if r.category_id == category_id]
    return filtered_records

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    for record in records:
        if record.id == record_id:
            records.remove(record)
            return {"detail": "Record deleted"}
    raise HTTPException(status_code=404, detail="Record not found")

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
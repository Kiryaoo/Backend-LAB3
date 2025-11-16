from fastapi import FastAPI, HTTPException, Query, Depends
from models import User, UserCreate, Category, CategoryCreate, Record, RecordCreate
from sqlalchemy.orm import Session
from database import get_db, init_db
from db_models import UserORM, CategoryORM, RecordORM
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import datetime

app = FastAPI(title="Expense Tracker API")

@app.lifespan("startup")
def on_startup():
    init_db()

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

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    obj = UserORM(name=user.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    obj = db.query(UserORM).filter(UserORM.id == user_id).first()
    if not obj:
        raise HTTPException(404, "User not found")
    return obj

@app.get("/users", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserORM).all()

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    obj = db.query(UserORM).filter(UserORM.id == user_id).first()
    if not obj:
        raise HTTPException(404, "User not found")
    db.delete(obj)
    db.commit()
    return JSONResponse(status_code=204, content=None)

@app.post("/categories/", response_model=Category, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    obj = CategoryORM(title=category.title)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    obj = db.query(CategoryORM).filter(CategoryORM.id == category_id).first()
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj

@app.get("/categories", response_model=list[Category])
def list_categories(db: Session = Depends(get_db)):
    return db.query(CategoryORM).all()

@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    obj = db.query(CategoryORM).filter(CategoryORM.id == category_id).first()
    if not obj:
        raise HTTPException(404, "Category not found")
    db.delete(obj)
    db.commit()
    return JSONResponse(status_code=204, content=None)

@app.post("/records/", response_model=Record, status_code=201)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    if not db.query(UserORM).filter(UserORM.id == record.user_id).first():
        raise HTTPException(404, "User not found")
    if not db.query(CategoryORM).filter(CategoryORM.id == record.category_id).first():
        raise HTTPException(404, "Category not found")
    obj = RecordORM(
        user_id=record.user_id,
        category_id=record.category_id,
        amount=record.amount,
        timestamp=record.timestamp
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/records/{record_id}", response_model=Record)
def get_record(record_id: int, db: Session = Depends(get_db)):
    obj = db.query(RecordORM).filter(RecordORM.id == record_id).first()
    if not obj:
        raise HTTPException(404, "Record not found")
    return obj

@app.get("/records", response_model=list[Record])
def list_records(user_id: int | None = Query(None, ge=1), category_id: int | None = Query(None, ge=1), db: Session = Depends(get_db)):
    query = db.query(RecordORM)
    if user_id is not None:
        query = query.filter(RecordORM.user_id == user_id)
    if category_id is not None:
        query = query.filter(RecordORM.category_id == category_id)
    return query.all()

@app.delete("/records/{record_id}", status_code=204)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    obj = db.query(RecordORM).filter(RecordORM.id == record_id).first()
    if not obj:
        raise HTTPException(404, "Record not found")
    db.delete(obj)
    db.commit()
    return JSONResponse(status_code=204, content=None)


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
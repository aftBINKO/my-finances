from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.responses import FileResponse
from starlette import status

from database import Session, engine
from sqlalchemy.orm import Session
from models import UserDB
# from .database import SessionLocal

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()


@app.get("/register", response_class=FileResponse)
def root_html():
    return "public/register.html"


@app.post("/register_ok", status_code=status.HTTP_201_CREATED)
#def hello(name = Body(embed=True)):
def register_ok(data = Body()):
    phone = data["phone"]
    password = data["password"]
    with Session(autoflush=False, bind=engine) as session:
        new_user = UserDB()
        new_user.phone = phone
        new_user.hashed_password = get_password_hash(password)
        session.add(new_user)
        session.commit()
    return {"status": status.HTTP_201_CREATED, "data": new_user}



# # Зависимость для получения сессии БД
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/register/")
# def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.username == username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Пользователь уже существует")
#     hashed_password = get_password_hash(password)
#     new_user = User(username=username, email=email, hashed_password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"msg": "Пользователь успешно зарегистрирован"}



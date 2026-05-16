import jwt
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer

from database import Session, engine
from sqlalchemy.orm import Session
from models import User

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Секретный ключ для подписи токенов
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"  # Алгоритм подписи
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена

# Функция для создания JWT-токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для проверки токена
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None  # Если токен недействителен или истёк


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/register", response_class=FileResponse)
def register_html():
    return "public/register.html"

@app.get("/login", response_class=FileResponse)
def register_html():
    return "public/login.html"


# Регистрация пользователя
@app.post("/register/")
def register_user(data = Body()):
    phone = data["phone"]
    password = data["password"]
    with Session(autoflush=False, bind=engine) as db:
        existing_user = db.query(User).filter(User.phone == phone).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")

        hashed_password = get_password_hash(password)
        new_user = User(phone=phone, hashed_password=hashed_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"msg": "Пользователь успешно зарегистрирован"}


@app.post("/login/")
def login(data = Body()):
    phone = data["phone"]
    password = data["password"]
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(User).filter(User.phone == phone).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        token_data = {"sub": user.phone}
        access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=30))
        print(access_token)
        return {"access_token": access_token, "token_type": "bearer"}

# Защищённый маршрут
@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")

    return {"msg": f"Добро пожаловать, {payload['sub']}!"}

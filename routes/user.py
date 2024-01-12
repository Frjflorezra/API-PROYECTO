from fastapi import Form, APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from typing import Annotated
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from pydantic import BaseModel
from passlib.context import CryptContext
from authentication import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from jose import JWTError, jwt

class UserLogin(BaseModel):
  email: str
  password: str

class TokenData(BaseModel):
    email: str | None = None

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

key = '1zRxydNdtCNvCPNaQ5NNWnmJhCQOz9mYH4BphnJgvR8='
f = Fernet(key)

user = APIRouter(prefix="/user",
    tags=["user"])

estructura = ("id_user", "name", "lastname", "email", "password")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

def authenticate_user(email: str, password: str):
    print(f"Attempting authentication for user with email: {email}")
    user = conn.execute(users.select().where(users.c.email == email)).first()

    if user and verify_password(password, user.password):
        print("Authentication successful")
        return user
    else:
        print("Authentication failed")
    return None

# def authenticate_user(email: str, password:str):
#     result = conn.execute(users.select().where(users.c.email == email)).first()
    
#     if result and verify_password(password, result.password):
#         return result
#     return None

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception
    user = conn.execute(users.select().where(users.c.email == token_data.email)).first() 
    if user is None:
        raise credentials_exception
    return user


@user.get("/")
def get_users():
    result = conn.execute(users.select()).fetchall()
    resultados = []
    for id, results in enumerate(result):
        prueba = dict(zip(estructura, results))
        resultados.append(prueba)
    return resultados

@user.get("/protected")
def me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}

@user.post("/")
async def create_user(user: User):

    result = conn.execute(users.select().where(users.c.email == user.email)).fetchone()
        
    if result:    
        
        raise HTTPException(status_code=400, detail="El correo electrónico ya existe.")
    
    else:
  
        new_user = dict(user)
        new_user['password'] = get_hashed_password(user.password)
        print(new_user)
        # new_user = {"nombre": user.nombre, "apellido": user.apellido, "correo": user.correo}
        # new_user["password"] = f.encrypt(user.password.encode("utf-8"))
        result = conn.execute(users.insert().values(new_user))
        conn.commit()
        cursor = conn.execute(users.select().where(users.c.id_user == result.lastrowid)).first()
        prueba = dict(zip(new_user.keys(),cursor))
    
    return prueba

# @user.post("/login")
# async def login_user(user: UserLogin):

#     result = conn.execute(users.select().where(users.c.email == user.email)).fetchone()
#     password = result.password
#     decrypt = f.decrypt(password).decode('utf-8')
    
#     if not result:
#         raise HTTPException(status_code=404, detail="El correo electrónico no existe.")

#   # Verificamos que la contraseña sea correcta.

#     if user.password != decrypt:
#         raise HTTPException(status_code=401, detail="La contraseña es incorrecta.")


@user.post("/token", response_model=Token)
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "id_user": user.id_user}

@user.get("/{id_user}")
def get_user(id_user: int):
    query = users.select().where(users.c.id_user == id_user)
    result = conn.execute(query).first()
    if result is None:
        return "No existe el usuario"
    prueba = dict(zip(estructura, result))
    return prueba

@user.put("/{id_usuario}")
async def update_user(user: User, id: int):
    password = f.encrypt(user.password.encode("utf-8"))
    conn.execute(users.update().values(name=user.name,lastname=user.lastname, email=user.email, password=password).where(users.c.id_user == id))
    conn.commit()
    query = users.select().where(users.c.id_user == id)
    result = conn.execute(query).first()
    prueba = dict(zip(estructura, result))
    return prueba


@user.delete("/{id_usuario}")
async def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id_user == id))
    conn.commit()
    query = users.select().where(users.c.id_user == id)
    result = conn.execute(query).first()
    if result is None:
        return "Eliminado"



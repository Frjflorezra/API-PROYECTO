from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet


key = Fernet.generate_key()
f = Fernet(key)
user = APIRouter(prefix="/user",
    tags=["user"])

estructura = ("id_usuario", "nombre", "apellido", "correo", "password")

@user.get("/")
def get_users():
    result = conn.execute(users.select()).fetchall()
    resultados = []
    for id, results in enumerate(result):
        prueba = dict(zip(estructura, results))
        resultados.append(prueba)
    return resultados


@user.post("/")
async def create_user(user: User):
    
    new_user = dict(user)
    new_user['password'] = f.encrypt(user.password.encode("utf-8"))
    print(new_user)
    # new_user = {"nombre": user.nombre, "apellido": user.apellido, "correo": user.correo}
    # new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    cursor = conn.execute(users.select().where(users.c.id_usuario == result.lastrowid)).first()
    prueba = dict(zip(new_user.keys(),cursor))
    
    return prueba


@user.get("/{id_usuario}")
def get_user(id_usuario: int):
    query = users.select().where(users.c.id_usuario == id_usuario)
    result = conn.execute(query).first()
    if result is None:
        return "No existe el usuario"
    prueba = dict(zip(estructura, result))
    return prueba

@user.put("/{id_usuario}")
async def update_user(user: User, id: int):
    password = f.encrypt(user.password.encode("utf-8"))
    conn.execute(users.update().values(nombre=user.nombre,apellido=user.apellido, correo=user.correo, password=password).where(users.c.id_usuario == id))
    conn.commit()
    query = users.select().where(users.c.id_usuario == id)
    result = conn.execute(query).first()
    prueba = dict(zip(estructura, result))
    return prueba


@user.delete("/{id_usuario}")
async def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id_usuario == id))
    conn.commit()
    query = users.select().where(users.c.id_usuario == id)
    result = conn.execute(query).first()
    if result is None:
        return "Eliminado"



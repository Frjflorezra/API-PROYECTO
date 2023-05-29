from fastapi import APIRouter
from config.db import conn
from models.proyectos import proyectos
from schemas.proyectos import Proyecto



proyecto = APIRouter(prefix="/proyectos", tags=["proyectos"])


estructura = ("id_proyecto", "nombre", "descripcion", "fecha_inicio", "fecha_final")


@proyecto.get("/")
async def get_project():
    result = conn.execute(proyectos.select()).fetchall()
    resultados = []
    for id, results in enumerate(result):
        prueba = dict(zip(estructura, results))
        resultados.append(prueba)
    return resultados


@proyecto.post("/")
async def create_project(proyecto: Proyecto):
    new_user = dict(proyecto)
    result = conn.execute(proyectos.insert().values(new_user))
    conn.commit()
    cursor = conn.execute(
        proyectos.select().where(proyectos.c.id_proyecto == result.lastrowid)
    ).first()
    prueba = dict(zip(new_user.keys(), cursor))
    return prueba


@proyecto.get("/{id}")
def get_project(id: int):
    query = proyectos.select().where(proyectos.c.id_proyecto == id)
    result = conn.execute(query).first()
    if result is None:
        return "No existe el proyecto"
    prueba = dict(zip(estructura, result))
    return prueba


@proyecto.put("/{id}")
async def update_project(proyecto: Proyecto, id: int):
    conn.execute(
        proyectos.update()
        .values(
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            fecha_inicio=proyecto.fecha_inicio,
            fecha_final=proyecto.fecha_final,
        )
        .where(proyectos.c.id_proyecto == id)
    )
    conn.commit()
    query = proyectos.select().where(proyectos.c.id_proyecto == id)
    result = conn.execute(query).first()
    prueba = dict(zip(estructura, result))
    return prueba


@proyecto.delete("/{id}")
async def delete_project(id: int):
    conn.execute(proyectos.delete().where(proyectos.c.id_proyecto == id))
    conn.commit()
    query = proyectos.select().where(proyectos.c.id_proyecto == id)
    result = conn.execute(query).first()
    if result is None:
        return "Proyecto eliminado"

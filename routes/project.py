from fastapi import APIRouter, Depends
from config.db import conn
from models.task import Projects
from schemas.project import Project
from schemas.user import User
from routes.user import get_current_user



projectBoard = APIRouter(prefix="/project", tags=["project"])


estructura = ("id_project", "title", "description", "start_date", "finish_date", "id_user")


@projectBoard.get("/")
async def get_project(current_user: User = Depends(get_current_user)):
    result = conn.execute(Projects.select().where(Projects.c.id_user == current_user.id_user)).fetchall()
    resultados = []
    for id, results in enumerate(result):
        prueba = dict(zip(estructura, results))
        resultados.append(prueba)
    return resultados


@projectBoard.post("/")
async def create_project(project: Project, current_user: User = Depends(get_current_user)):
    id_user = current_user.id_user
    new_user = dict(project, id_user=id_user)
    print (new_user)
    result = conn.execute(Projects.insert().values(new_user))
    conn.commit()
    cursor = conn.execute(
        Projects.select().where(Projects.c.id_project == result.lastrowid)
    ).first()
    prueba = dict(zip(new_user.keys(), cursor))
    return prueba


@projectBoard.get("/{id}")
def get_project(id: int, current_user: User = Depends(get_current_user)):
  if id == current_user.id_user:  
    query = Projects.select().where(Projects.c.id_project == id, Projects.c.id_user == current_user.id_user)
    result = conn.execute(query).first()
    if result is None:
        return "No existe el proyecto"
    prueba = dict(zip(estructura, result))
    return prueba


@projectBoard.put("/{id}")
async def update_project(project: Project, id: int, current_user: User = Depends(get_current_user)):
    conn.execute(
        Projects.update()
        .values(
            title=project.title,
            description=project.description,
            start_date=project.start_date,
            finish_date=project.finish_date
        )
        .where(Projects.c.id_project == id, Projects.c.id_user == current_user.id_user)
    )
    conn.commit()
    query = Projects.select().where(Projects.c.id_project == id)
    result = conn.execute(query).first()
    prueba = dict(zip(estructura, result))
    return prueba


@projectBoard.delete("/{id}")
async def delete_project(id: int, current_user: User = Depends(get_current_user)):
    conn.execute(Projects.delete().where(Projects.c.id_project == id, Projects.c.id_user == current_user.id_user))
    conn.commit()
    query = Projects.select().where(Projects.c.id_project == id, Projects.c.id_user == current_user)
    result = conn.execute(query).first()
    if result is None:
        return "Proyecto eliminado"

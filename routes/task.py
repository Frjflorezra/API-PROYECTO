from fastapi import APIRouter, Depends, HTTPException
from config.db import conn
from models.task import Tasks, Projects
from schemas.task import Task
from routes.user import get_current_user
from schemas.user import User

task = APIRouter(prefix= "/project/{id_project}/task", tags=["task"])


estructura = ("id_task", "title", "description", "status", "id_project")


@task.get("/")
async def get_task(id_project: int, current_user: User = Depends(get_current_user)):
    project = conn.execute(Projects.select().where(Projects.c.id_project == id_project, Projects.c.id_user == current_user.id_user)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = conn.execute(Tasks.select().where(Tasks.c.id_project == id_project)).fetchall()
    resultados = []
    for id, results in enumerate(result):
        prueba = dict(zip(estructura, results))
        resultados.append(prueba)
    return resultados


@task.post("/")
async def create_task(task: Task, id_project: int,  current_user: User = Depends(get_current_user)):

    project = conn.execute(Projects.select().where(Projects.c.id_project == id_project, Projects.c.id_user == current_user.id_user)).fetchone()
    id = project.id_project
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    new_user = dict(task, id_project = id)
    result = conn.execute(Tasks.insert().values(new_user))
    conn.commit()
    cursor = conn.execute(
        Tasks.select().where(Tasks.c.id_task == result.lastrowid)
    ).first()
    prueba = dict(zip(new_user.keys(), cursor))
    return prueba


@task.get("/{id}")
def get_task(id: int, id_project: int,  current_user: User = Depends(get_current_user)):
    project = conn.execute(Projects.select().where(Projects.c.id_project == id_project, Projects.c.id_user == current_user.id_user)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    query = Tasks.select().where(Tasks.c.id_task == id)
    result = conn.execute(query).first()
    if result is None:
        return "No existe el proyecto"
    prueba = dict(zip(estructura, result))
    return prueba


@task.put("/{id}")
async def update_task(task: Task, id: int, id_project: int,  current_user: User = Depends(get_current_user)):
    project = conn.execute(Projects.select().where(Projects.c.id_project == id_project, Projects.c.id_user == current_user.id_user)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    conn.execute(
        Tasks.update()
        .values(
            title=task.title,
            description=task.description,
            status=task.status
        )
        .where(Tasks.c.id_project == id_project, Tasks.c.id_task == id )
    )
    conn.commit()
    query = Tasks.select().where(Tasks.c.id_task == id, Tasks.c.id_project == id_project)
    result = conn.execute(query).first()
    prueba = dict(zip(estructura, result))
    return prueba


@task.delete("/{id}")
async def delete_task(id: int, id_project: int,  current_user: User = Depends(get_current_user)):
    project = conn.execute(Projects.select().where(Projects.c.id_project == id_project, Projects.c.id_user == current_user.id_user)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    conn.execute(Tasks.delete().where(Tasks.c.id_task == id, Tasks.c.id_project == id_project ))
    conn.commit()
    query = Tasks.select().where(Tasks.c.id_task == id)
    result = conn.execute(query).first()
    if result is None:
        return "Task delete"

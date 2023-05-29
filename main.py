from fastapi import FastAPI
from routes.user import user
from routes.proyectos import proyecto

app = FastAPI()

app.include_router(user)
app.include_router(proyecto)


# ruta de inicio http://127.0.0.1:8000/

# ruta doc http://127.0.0.1:8000/docs#/

from fastapi import FastAPI
from routes.user import user
from routes.project import projectBoard
from routes.task import task


# adding cors hader
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#adding cors urls

origins = [
    'http://localhost:3000'
]
# add moiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user)
app.include_router(projectBoard)
app.include_router(task)


# ruta de inicio http://127.0.0.1:8000/

# ruta doc http://127.0.0.1:8000/docs#/

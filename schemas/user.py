from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id_usuario:Optional[str]
    nombre:str
    apellido:str
    correo:str
    password:str




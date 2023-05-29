from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Proyecto(BaseModel):
    id_proyecto:Optional[int]
    nombre:str
    descripcion:str
    fecha_inicio:datetime
    fecha_final:datetime
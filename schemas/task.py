from pydantic import BaseModel
from typing import Optional
from sqlalchemy.sql.sqltypes import enum


class Task(BaseModel):
    id_task:Optional[int]
    title:str
    description:str
    status:str

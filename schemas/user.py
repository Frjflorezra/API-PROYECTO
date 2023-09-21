from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id_user:Optional[str]
    name:str
    lastname:str
    email:str
    password:str





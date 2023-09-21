from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Project(BaseModel):
    id_project:Optional[int]
    title:str
    description:str
    start_date:datetime
    finish_date:datetime
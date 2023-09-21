from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Relationship
from config.db import meta, engine
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Enum

Projects = Table(
    "project",
    meta,
    Column("id_project", Integer, primary_key=True),
    Column("title", String(255)),
    Column("description", String(255)),
    Column("start_date", DateTime),
    Column("finish_date", DateTime),
    Column("id_user", Integer, ForeignKey('users.id_user'))
)
users = Relationship('users', back_populates='project')

Tasks = Table(
    "task",
    meta,
    Column("id_task", Integer, primary_key=True),
    Column("title", String(255)),
    Column("description", String(255)),
    Column("status", Enum('Unstarted', 'Started', 'Completed')),
    Column("id_project", Integer, ForeignKey('project.id_project'))
)
project = Relationship('project', back_populates='task')

meta.create_all(engine)
from sqlalchemy import Table, Column
from config.db import meta, engine
from sqlalchemy.sql.sqltypes import Integer, String

users = Table(
    "users",
    meta,
    Column("id_usuario", Integer, primary_key=True),
    Column("nombre", String(255)),
    Column("apellido", String(255)),
    Column("correo", String(100)),
    Column("password", String(255)),
)

meta.create_all(engine)
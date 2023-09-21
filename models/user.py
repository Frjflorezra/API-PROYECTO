from sqlalchemy import Table, Column
from config.db import meta, engine
from sqlalchemy.sql.sqltypes import Integer, String

users = Table(
    "users",
    meta,
    Column("id_user", Integer, primary_key=True),
    Column("name", String(255)),
    Column("lastname", String(255)),
    Column("email", String(100)),
    Column("password", String(255)),
)

meta.create_all(engine)

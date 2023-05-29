from sqlalchemy import Table, Column
from config.db import meta, engine
from sqlalchemy.sql.sqltypes import Integer, String, Date, DATETIME

proyectos = Table(
    "proyectos",
    meta,
    Column("id_proyecto", Integer, primary_key=True),
    Column("nombre", String(255)),
    Column("descripcion", String(255)),
    Column("fecha_inicio", Date),
    Column("fecha_final", Date),
)

meta.create_all(engine)
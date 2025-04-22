from sqlalchemy import MetaData, Table, Column, Integer, Text

metadata = MetaData()

# mirror the Alembic migration
pokemon = Table(
    'pokemon', metadata,
    Column('id',      Integer, primary_key=True),
    Column('name',    Text,    nullable=False),
    Column('species', Text),
    Column('power',   Integer),
)

rick_morty_char = Table(
    'rick_morty_char', metadata,
    Column('id',      Integer, primary_key=True),
    Column('name',    Text,    nullable=False),
    Column('status',  Text),
    Column('species', Text),
)

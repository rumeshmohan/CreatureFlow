import os, asyncio, json
from aiokafka import AIOKafkaConsumer
from sqlalchemy import Table, Column, Integer, Text, MetaData
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")
KAFKA = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# define tables (must match create_tables.py)
metadata = MetaData()

pokemon = Table(
    "pokemon", metadata,
    Column("id",      Integer, primary_key=True),
    Column("name",    Text,    nullable=False),
    Column("species", Text),
    Column("power",   Integer),
)

rick_morty_char = Table(
    "rick_morty_char", metadata,
    Column("id",      Integer, primary_key=True),
    Column("name",    Text,    nullable=False),
    Column("status",  Text),
    Column("species", Text),
)

async def consume():
    consumer = AIOKafkaConsumer(
        "raw-pokemon", "raw-characters",
        bootstrap_servers=KAFKA,
        group_id="processor-group"
    )
    await consumer.start()
    engine = create_async_engine(DATABASE_URL, echo=False)
    # ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            async with engine.begin() as conn:
                if msg.topic == "raw-pokemon":
                    # simple power calculation
                    power = len(data["name"])
                    poke_id = int(data["url"].rstrip("/").split("/")[-1])
                    await conn.execute(
                        pokemon.insert().values(
                            id=poke_id,
                            name=data["name"],
                            species=data["name"].lower(),
                            power=power
                        )
                    )
                else:
                    await conn.execute(
                        rick_morty_char.insert().values(
                            id=int(data["id"]),
                            name=data["name"],
                            status=data.get("status"),
                            species=data.get("species")
                        )
                    )
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())

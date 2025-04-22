import json
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from fastapi_limiter.depends import RateLimiter
from .cache import init_redis, redis
from .db import AsyncSessionLocal
from .models import pokemon, rick_morty_char
from .schemas import Pokemon, Character


app = FastAPI(on_startup=[init_redis])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get(
    "/pokemon",
    response_model=list[Pokemon],
    summary="List Pokémon",
    description="Paginated list via `limit` and `cursor`.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def list_pokemon(
    limit: int = Query(50, le=100),
    cursor: Optional[int] = None,
    db=Depends(get_db)
):
    key = f"pokemon:{limit}:{cursor or 0}"
    cached = await redis.get(key)
    if cached:
        items = json.loads(cached)
        return [Pokemon.model_validate(i) for i in items]

    stmt = select(pokemon).order_by(pokemon.c.id).limit(limit)
    if cursor:
        stmt = stmt.where(pokemon.c.id > cursor)
    result = await db.execute(stmt)
    records = result.scalars().all()

    to_cache = [r.model_dump() for r in records]
    await redis.set(key, json.dumps(to_cache), ex=60)
    return records

@app.get(
    "/pokemon/{poke_id}",
    response_model=Pokemon,
    summary="Get one Pokémon",
    dependencies=[Depends(RateLimiter(times=20, seconds=60))]
)
async def get_pokemon(poke_id: int, db=Depends(get_db)):
    stmt = select(pokemon).where(pokemon.c.id == poke_id)
    result = await db.execute(stmt)
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return row

@app.get(
    "/characters",
    response_model=list[Character],
    summary="List Characters",
    dependencies=[Depends(RateLimiter(times=20, seconds=60))]
)
async def list_characters(
    status: Optional[str]  = None,
    species: Optional[str] = None,
    db=Depends(get_db)
):
    key = f"chars:{status or 'any'}:{species or 'any'}"
    cached = await redis.get(key)
    if cached:
        items = json.loads(cached)
        return [Character.model_validate(i) for i in items]

    stmt = select(rick_morty_char)
    if status:
        stmt = stmt.where(rick_morty_char.c.status == status)
    if species:
        stmt = stmt.where(rick_morty_char.c.species == species)
    result = await db.execute(stmt)
    records = result.scalars().all()

    to_cache = [r.model_dump() for r in records]
    await redis.set(key, json.dumps(to_cache), ex=60)
    return records

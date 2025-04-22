import os, asyncio, json
import httpx
from aiokafka import AIOKafkaProducer

KAFKA = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INTERVAL = int(os.getenv("POLL_INTERVAL", 60))

async def produce():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA)
    await producer.start()
    try:
        while True:
            async with httpx.AsyncClient() as client:
                resp = await client.get("https://pokeapi.co/api/v2/pokemon?limit=100")
                data = resp.json().get("results", [])
                for item in data:
                    await producer.send_and_wait("raw-pokemon", json.dumps(item).encode())
            await asyncio.sleep(INTERVAL)
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(produce())

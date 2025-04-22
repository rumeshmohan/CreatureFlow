import os, asyncio, json
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from aiokafka import AIOKafkaProducer

KAFKA = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INTERVAL = int(os.getenv("POLL_INTERVAL", 60))

query = gql("""
query ($page: Int!) {
  characters(page: $page) {
    results { id name status species }
  }
}
""")

async def produce():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA)
    await producer.start()
    transport = AIOHTTPTransport(url="https://rickandmortyapi.com/graphql")
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        try:
            while True:
                result = await session.execute(query, variable_values={"page": 1})
                for item in result["characters"]["results"]:
                    await producer.send_and_wait("raw-characters", json.dumps(item).encode())
                await asyncio.sleep(INTERVAL)
        finally:
            await producer.stop()

if __name__ == "__main__":
    asyncio.run(produce())

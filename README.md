# TIKOS

**CreatureFlow**

> A microservices-based “creature” data aggregator: ingests Pokémon and Rick & Morty characters, processes and stores them in Postgres, and exposes a FastAPI service.

## Table of Contents

1. [About](#about)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
   - [Docker Compose](#docker-compose)  
   - [Local Development](#local-development)  
5. [API](#api)  
6. [Configuration](#configuration)  
7. [License](#license)  


---

## About

TIKOS’s **creature‑aggregator** suite ingests data from two public APIs (PokéAPI and Rick & Morty GraphQL), streams raw items into Kafka, processes them into structured tables, and serves them via a FastAPI endpoint. It demonstrates:

- Async data ingestion (REST & GraphQL)  
- Kafka-based message pipelines  
- Async database access with SQLAlchemy + Alembic  
- Containerized microservices with Docker Compose  

## Features

- **GraphQL Ingestor**: polls the Rick & Morty GraphQL API, publishes to `raw-characters` topic  
- **REST Ingestor**: polls the PokéAPI REST endpoint, publishes to `raw-pokemon` topic  
- **Processor**: consumes both `raw-pokemon` and `raw-characters`, computes “power” for Pokémon, writes into Postgres tables  
- **API**: FastAPI service exposing CRUD‑style endpoints in `api/`  
- **Persistence**: Postgres for storage, Redis for caching, Kafka for messaging, Alembic for migrations  

- **Postgres**: stores `pokemon` & `rick_morty_char` tables  
- **Redis**: optional caching layer for API  
- **Zookeeper+Kafka**: message broker  
- **Docker Compose** orchestrates all components  

---

## Installation

### Prerequisites

- [Docker Engine & Docker Compose v2+](https://docs.docker.com/get-docker/)  
- *(Optional)* Python 3.9+ & `pip`

### Clone the repo

```bash
git clone https://github.com/rumeshmohan/CreatureFlow.git
cd CreatureFlow/creature-aggregator
```

## Usage

### Docker Compose

Build and start everything (Postgres, Redis, Zookeeper, Kafka, ingestors, processor, API):

```bash
docker-compose up --build
```

- API available at ➜ http://localhost:8000  
- Swagger UI at ➜ http://localhost:8000/docs  
- To run in background:  
  ```bash
  docker-compose up -d --build
  ```

### Local Development (without Docker)

1. **Initialize the database**  
   ```bash
   python create_tables.py
   # or, with Alembic:
   alembic upgrade head
   ```

2. **Run Postgres, Redis & Kafka**  
   Use your local services or spin up with Docker:
   ```bash
   docker run -d -p 5432:5432 -e POSTGRES_USER=pguser -e POSTGRES_PASSWORD=pgpass -e POSTGRES_DB=creatures postgres:15
   docker run -d -p 6379:6379 redis:7
   # For Kafka & Zookeeper, you can use Docker Compose or Bitnami images
   docker-compose up -d zookeeper kafka
   ```

3. **API**  
   ```bash
   cd api
   pip install -r requirements.txt
   export DATABASE_URL="postgresql+asyncpg://pguser:pgpass@localhost:5432/creatures"
   export REDIS_URL="redis://localhost:6379"
   uvicorn api.main:app --reload
   ```

4. **GraphQL Ingestor**  
   ```bash
   cd ingestor_gql
   pip install -r requirements.txt
   export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
   python main.py
   ```

5. **REST Ingestor**  
   ```bash
   cd ingestor_rest
   pip install -r requirements.txt
   export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
   python main.py
   ```

6. **Processor**  
   ```bash
   cd processor
   pip install -r requirements.txt
   export DATABASE_URL="postgresql+asyncpg://pguser:pgpass@localhost:5432/creatures"
   export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
   python main.py
   ```

---

## API

Once running, browse the interactive Swagger docs:

```
http://localhost:8000/docs
```

Endpoints include:

- `GET /pokemon/`  
- `GET /rick_morty_char/`  
- `POST /pokemon/` etc.

*(See `api/main.py` for full route list.)*

---

## Configuration

All services use environment variables. Default values are in each service’s `Dockerfile` or code:

| Variable                   | Default                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| `POSTGRES_USER`            | `pguser`                                                                                 |
| `POSTGRES_PASSWORD`        | `pgpass`                                                                                 |
| `POSTGRES_DB`              | `creatures`                                                                              |
| `DATABASE_URL`             | `postgresql+asyncpg://pguser:pgpass@postgres:5432/creatures`                             |
| `REDIS_URL`                | `redis://redis:6379`                                                                     |
| `KAFKA_BOOTSTRAP_SERVERS`  | `kafka:9092` (or `localhost:9092` for local dev)                                         |
| `POLL_INTERVAL`            | `60` seconds between ingestor fetches                                                    |

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

```

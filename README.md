# Ngafalinfy

Ngafalinfy is a flashcard app built with FastAPI and SQLAlchemy, designed to help you memorize vocabulary using spaced repetition.  
It uses Alembic for database migrations and follows modern Python development practices with PDM.

---

## 📦 Main Packages

- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM
- [Alembic](https://alembic.sqlalchemy.org/) – Database migrations
- [Pydantic](https://docs.pydantic.dev/) – Data validation
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Env var loader
- [PyMySQL](https://pypi.org/project/PyMySQL/) – MySQL driver

### Dev Tools
- [PDM](https://pdm-project.org/en/latest/) – Python package/dependency manager
- [Ruff](https://docs.astral.sh/ruff/) – Linter
- [Black](https://black.readthedocs.io/) – Formatter
- [Pyright](https://microsoft.github.io/pyright/) – Type checker
- [Pytest](https://docs.pytest.org/en/stable/) – Testing framework

---

## 🛠️ Requirements

- [Docker](https://www.docker.com/) & Docker Compose
- [Python 3.13](https://www.python.org/) (if you want to run outside Docker)
- [PDM](https://pdm.fming.dev/latest/#installation) (if you want to run locally)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/alamsyah10/ngafalinfy.git
cd ngafalinfy
```
### 2. Copy Environment Variables
```bash
cp .env.example .env.docker
```
Edit .env.docker if needed (e.g. DB password, CORS origins).
### 3. Run with Docker Compose
```bash
docker compose up --build
```
This will start:
- ngafalinfy-api → FastAPI app (port 8080)
- ngafalinfy-db → MySQL database (port 3306)
### 4. Check the Server
- Health check: http://localhost:8080/health
- Interactive API docs: http://localhost:8080/docs
- Alternative docs (ReDoc): http://localhost:8080/redoc

## 🧰 Useful Scripts (via PDM)
```bash
pdm run format      # Format code with Ruff
pdm run lint        # Lint (ruff + pyright)
pdm run test        # Run pytest
pdm run check       # Run format + lint + test
```
### Alembic migrations
```bash
pdm run alembic revision --autogenerate -m "add new table"
pdm run alembic upgrade head
pdm run alembic downgrade -1
```

## 🗄️ Database
- Default: MySQL (containerized in docker-compose.yaml)
- Credentials are loaded from .env.docker:
```env
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=password
MYSQL_HOST=ngafalinfy-db
MYSQL_DATABASE=ngafalinfy
```

## 📝 Project Structure
```bash
.
├── alembic/             # Alembic migrations
├── certs/               # Certificates
├── docker/              # Dockerfiles (api + db)
├── log/                 # Log files
├── scripts/             # Startup / helper scripts
├── src/
│   ├── api/             # API routers
│   ├── infrastructure/  # DB/session/config helpers
│   ├── models/          # SQLAlchemy models
│   ├── config.py        # Settings loader
│   ├── main.py          # FastAPI entrypoint
│   └── __init__.py
├── tests/               # Pytest tests
├── docker-compose.yaml  # Services definition
├── pyproject.toml       # PDM + tool configs
├── pdm.lock             # Locked dependencies
├── .env.docker          # Docker environment
├── .env.example         # Example environment
└── README.md
```

## 📜 License
MIT License © 2025 Ngafalinfy Contributors

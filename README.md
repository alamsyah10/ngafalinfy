# 📚 Ngafalinfy

Ngafalinfy is a flashcard app built with **FastAPI** and **SQLAlchemy**, designed to help you memorize vocabulary using spaced repetition.  
It uses **Alembic** for database migrations and follows modern Python development practices with **PDM**.

---

## 📦 Main Packages

- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM
- [Alembic](https://alembic.sqlalchemy.org/) – Database migrations
- [Pydantic](https://docs.pydantic.dev/) – Data validation
- [PyMySQL](https://pypi.org/project/PyMySQL/) – MySQL driver
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment variable loader

### 🛠️ Dev Tools
- [PDM](https://pdm-project.org/en/latest/) – Dependency manager
- [Ruff](https://docs.astral.sh/ruff/) – Linter
- [Black](https://black.readthedocs.io/) – Code formatter
- [Pyright](https://microsoft.github.io/pyright/) – Type checker
- [Pytest](https://docs.pytest.org/en/stable/) – Testing framework

---

## ⚙️ Requirements

- [Docker](https://www.docker.com/) & Docker Compose
- [Python 3.13](https://www.python.org/) (for running outside Docker)
- [PDM](https://pdm.fming.dev/latest/#installation) (for local development)

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
- Health check: http://localhost:8080/checkhealth
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
    SQL_LOGGING=false
    MYSQL_HOST=ngafalinfy-db
    MYSQL_USER=your_mysql_user
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_DATABASE=ngafalinfy
    ```

## 🔑 Google OAuth Setup

1. Go to **Google Cloud Console → APIs & Services → Credentials**  
2. Create an **OAuth 2.0 Client ID** (Web application)  
3. Add this to **Authorized redirect URIs**:
   ```bash
   http://localhost:8080/auth/google/callback
   ```
   > Use your production domain when deploying.  
4. Copy the **Client ID** and **Client Secret** into your `.env`
- Example configuration:
  ```env
  GOOGLE_CLIENT_ID=your_google_client_id
  GOOGLE_CLIENT_SECRET=your_google_client_secret
  GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
  ```

## 🔐 Session & Cookie Notes

- `SESSION_SECRET` must be **at least 32 characters** in production.  
- For HTTPS deployments, set:
  ```env
  SESSION_SAMESITE=none
  SESSION_HTTPS_ONLY=true
  ```


## 📝 Project Structure
```bash
.
├── alembic/  
├── certs/ 
├── docker/  
│   ├── api/
│   └── db/
├── log/  
├── scripts/ 
├── src/
│   ├── api/
│   │   ├── composition/ 
│   │   ├── error_schema/ 
│   │   ├── log/ 
│   │   ├── middleware/ 
│   │   └── router/ 
│   ├── domain/ 
│   ├── infrastructure/ 
│   │   ├── db/
│   │   └── security/
│   ├── config.py
│   ├── main.py
│   └── __init__.py
├── tests/
├── docker-compose.yaml
├── pyproject.toml
├── pdm.lock
├── .env.example
└── README.md
```

## 📜 License
MIT License © 2025 Ngafalinfy Contributors

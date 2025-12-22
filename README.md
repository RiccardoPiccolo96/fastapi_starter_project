# 🚀 FastAPI Modern Starter

A professional, production-ready backend boilerplate built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, and **Alembic**, managed by the high-performance **uv** package manager.

## 📝 Description
This application provides a robust foundation for building scalable asynchronous APIs. It features a modular structure, automated database migrations, and a pre-configured development environment. 

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/).
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/).

---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have **uv** installed on your system then install all required packages:
```bash
uv sync
```
----

# ⚗️ Alembic Operations Guide (Asynchronous)

This document provides the standard procedure for managing database migrations using **Alembic** within an asynchronous **SQLAlchemy** environment.


## 1. Environment Initialization
To set up the migration structure for the first time, execute the following command in the project root:
```bash
alembic init -t async alembic
```
### 2. Configuration of env.py
The env.py script is the bridge between Alembic and your application logic. The following manual adjustments are required:

A. Database Connection (Row ~22)
Ensure the database URL is dynamically pulled from your application settings to maintain environment consistency:
```python
from app.core.config import settings
# ...
config.set_main_option("sqlalchemy.url", str(settings.database_url))
```
B. Model Metadata (Row ~31)
Import the declarative Base to enable schema detection:
```python
from app.models import Base 
# ...
target_metadata = Base.metadata
```
**Note**: Ensure all models are imported in app/models/__init__.py. If a model is not imported, Alembic will not detect the table and might generate a script to drop it.

### 3. Generating a Migration Script
Whenever the SQLAlchemy models are modified, generate a new revision script:
```bash
alembic revision --autogenerate -m "Initial migration"
```

### 4. Applying Migration
To synchronize the physical database schema with the latest migration scripts:
```bash
python -m alembic upgrade head
```

----

# 🛠️ VS Code Debugging & Environment Configuration

To streamline development and debugging in Visual Studio Code, you should configure the `launch.json` file and use structured environment files.


### 1. VS Code Launch Configuration
The `launch.json` file allows you to start your FastAPI application directly from VS Code with the debugger attached. This enables you to set breakpoints and inspect variables in real-time.

Create or edit the file at `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI - Dev",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "env": {
                "ENV": "DEV",
                "DEBUG": "True"
            },
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```
### 2. Environment Variables Strategy
For better security and organization, the project uses stage-specific environment files. These files contain sensitive data and should follow this naming convention:
|File Name    |	Environment | Usage |
| :---------- | :---------: | :---- |
|.env.dev     |Development  | Local machine, includes debug logs.|
|.env.staging |	Staging     | Pre-production testing environment.|
|.env.prod    | Production  | Live production server (strictly secured)

### 3. Example file .env.dev
```text
# App Config
APP_NAME=FastAPI App
APP_VERSION=1.0.0
ENV=DEV
DEBUG=True

#CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

DB_HOST=localhost
DB_PORT=3308
DB_USER=user
DB_PASSWORD=password
DB_NAME=default

# External Client
SERIES_TV_URL=https://api.tvmaze.com
```

### **Run Via Command Line**
By default it will load .env.dev file
``` bash
uv run uvicorn app.main:app --reload
```

---

## 🐳 Docker Deployment

This project uses **Docker Compose** to orchestrate the FastAPI application and the MySQL database in an isolated environment.

### 🛠️ Prerequisites
- Docker and Docker Compose installed.
- A valid `.env_docker.dev` file in the root directory (containing DB credentials).

### 🚀 Commands

To build and start the entire stack, use the following command:

```bash
docker-compose --env-file .env_docker.dev up --build
```

### .env.docker.dev file
```json
# App Config
APP_NAME=FastAPI App
APP_VERSION=1.0.0
ENV=DEV
DEBUG=True

#CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

DB_HOST=mysql # docker url db
DB_PORT=3306  # docker port db
DB_USER=user
DB_PASSWORD=password
DB_NAME=default

# External Client
SERIES_TV_URL=https://api.tvmaze.com
```
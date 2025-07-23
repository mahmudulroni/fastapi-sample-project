# FastAPI Sample Project

A modular and scalable FastAPI boilerplate project using SQLModel, Alembic, and modern Python standards. It features organized routing, service layers, and migration support.

---

## 🚀 Quick Start

### 1. Create Virtual Environment (via `uv`)

```bash
uv venv
```

### 2. Activate Virtual Environment

```bash
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
uv pip install -e .
```

### 4. Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add the generated key to your `.env` file.

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

### 6. Database Migrations

```bash
alembic revision --autogenerate -m "<message>"
alembic upgrade head
```

---

## 📁 Project Architecture

```
fastapi-sample-project/
|
├── app/
│   ├── alembic/                  # Alembic migration scripts
│   │   ├── versions/             # Auto-generated migration versions
│   │   └── env.py                # Alembic environment setup
│   │
│   ├── api/                      # Main router collector
│   │   └── routes.py
│   │
│   ├── core/                     # Core configs
│   │   ├── config.py             # Pydantic-based settings
│   │   ├── database.py           # DB engine/session setup
│   │   └── security.py           # Auth helpers
│   │
│   ├── modules/                  # Feature-specific modules
│   │   ├── models/               # SQLModel definitions
│   │   ├── routes/               # FastAPI routers
│   │   ├── schemas/              # Pydantic request/response models
│   │   └── services/             # Business logic
│   │
│   ├── shared/                   # Shared utilities
│   │   ├── base_model.py         # UUID, timestamps, etc.
│   │   ├── schemas.py            # Common schemas
│   │   └── utils.py              # Helper functions
│   │
│   ├── dependency.py             # Shared FastAPI dependencies
│   └── main.py                   # FastAPI app instance
│
├── .env                          # Environment variables
├── alembic.ini                   # Alembic config
├── pyproject.toml                # Project dependencies
└── README.md
```

---

## 🧩 Tech Stack

* **Python 3.10+**
* **FastAPI**
* **SQLModel** (SQLAlchemy + Pydantic)
* **Alembic** (DB migrations)
* **Uvicorn** (ASGI server)
* **Hatch + uv** (Environment & packaging)

---

## 📌 Features

* Modular app layout
* JWT-based authentication
* Secure password hashing
* Alembic migration support
* SQLModel with async-ready setup

---

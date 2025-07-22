# FastAPI Sample Project

### Insatll `venv` or virtual environment
```
uv venv
```

### Activate virtual environment
```
source.venv/bin/activate # On Linux/macOS
```
```
.venv\Scripts\activate # On Windows
```

### Install all dependency or packages using `uv`
```
uv pip install -e .
```

### Generate secret key and add it to the `.env`
```
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Run the project
```
uvicorn app.main:app --reload
```
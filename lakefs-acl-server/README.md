# lakefs-acl-server

ACL-management service for lakeFS, built with FastAPI.

## Features
- FastAPI app skeleton
- Health check endpoint (`/health`)
- Planned: CRUD for users, groups, policies, credentials
- Configurable database (PostgreSQL)

## Quickstart (local, with venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install uv
uv pip install --system --no-cache-dir
uvicorn app.main:app --reload
```

Open: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

## Quickstart (Docker)

```bash
cd lakefs-acl-server
# Build image
sudo docker build -t lakefs-acl-server .
# Run
sudo docker run -it --rm -p 8000:8000 lakefs-acl-server
```

App will be at [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## Next steps
- DB config via env vars/dotenv
- Implement user/group/policy/credential models & APIs
- Add tests, Alembic migrations

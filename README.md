# AI Support Workflow (Dockerized)

Components:
- FastAPI backend (webhook, DB)
- PostgreSQL
- Redis
- Celery worker
- Flower (monitoring)
- n8n (workflow editor)

## Quickstart (development)

1. Copy environment and set values:
   ```bash
   cp .env.example .env
   # edit .env -> set OPENAI_API_KEY, N8N_PASSWORD, etc.

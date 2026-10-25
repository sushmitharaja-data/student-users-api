# Student Users API

A beginner-friendly Python and FastAPI REST API for managing users in SQLite.

## Run & Operate

- `pip install -r requirements.txt` — install the Python dependencies
- `uvicorn main:app --reload` — run the API locally
- `pnpm --filter @workspace/api-server run dev` — run the API through the Replit preview
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- Swagger UI: `http://127.0.0.1:8000/docs`
- SQLite file: `users.db` (created automatically)
- Replit preview API prefix: `/api`

## Stack

- Python, FastAPI, Pydantic, SQLite, and Uvicorn
- The surrounding Replit project uses pnpm workspaces for its shared tooling

## Where things live

- `main.py` — API routes, request validation, and SQLite setup
- `requirements.txt` — Python dependencies
- `README.md` — setup guide and API endpoint documentation

## Architecture decisions

- The API uses Python's built-in `sqlite3` module to keep the example easy to follow.
- Root routes match the assignment; hidden `/api` aliases support the Replit API preview path.

## Product

- Create, list, update, and delete users with validated names and email addresses.

## User preferences

- Keep this project beginner-friendly and API-only; do not add a frontend.

## Gotchas

- The Replit preview uses `/api` as a routing prefix. When running locally, use the unprefixed routes in `README.md`.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details

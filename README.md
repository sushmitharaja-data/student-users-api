# Student Users API

A beginner-friendly REST API built with Python and FastAPI. It stores users in a local SQLite database and supports creating, listing, updating, and deleting users. There is no frontend.

## Requirements

- Python 3.10 or newer
- pip

## Setup and run

From the project root:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. The `users.db` SQLite file and its `users` table are created automatically the first time the API starts.

Open Swagger UI at `http://127.0.0.1:8000/docs`. FastAPI also provides the OpenAPI schema at `http://127.0.0.1:8000/openapi.json`.

## User fields

| Field | Type | Rules |
| --- | --- | --- |
| `id` | integer | Generated automatically |
| `name` | string | Required, 1–100 characters; surrounding whitespace is removed |
| `email` | string | Required, must be a valid email, and must be unique |

## API endpoints

All request and response bodies use JSON.

| Method | Path | Description | Success response |
| --- | --- | --- | --- |
| `POST` | `/users` | Create a user | `201 Created` with the new user |
| `GET` | `/users` | List all users | `200 OK` with a list |
| `PUT` | `/users/{user_id}` | Replace a user's name and email | `200 OK` with the updated user |
| `DELETE` | `/users/{user_id}` | Delete a user | `204 No Content` |

`POST /users` and `PUT /users/{user_id}` require both `name` and `email`:

```json
{
  "name": "Alex Student",
  "email": "alex@example.com"
}
```

### Example requests

Create a user:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex Student","email":"alex@example.com"}'
```

List users:

```bash
curl http://127.0.0.1:8000/users
```

Update user with ID `1`:

```bash
curl -X PUT http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex S.","email":"alex@example.com"}'
```

Delete user with ID `1`:

```bash
curl -X DELETE http://127.0.0.1:8000/users/1
```

### Errors

- `404 Not Found` — the requested user ID does not exist.
- `409 Conflict` — the email address is already in use.
- `422 Unprocessable Entity` — the request body is missing required fields or has an invalid name or email.

## Replit preview

The API is available through the `/api` preview prefix in this project. For example, use `/api/users` and `/api/docs` in the preview. When running the API locally with the commands above, use the unprefixed paths shown in the endpoint table.

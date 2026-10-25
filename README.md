# Student Users API

A beginner-friendly REST API built with Python and FastAPI. It stores users in a local SQLite database and supports creating, listing, updating, and deleting users. There is no frontend.

## Requirements

- Python 3.10 or newer
- pip

## Setup and run

From the project root:

```bash
pip install -r requirements.txt
# Set these in your shell before starting the API:
export API_USERNAME="your-username"
export API_PASSWORD="your-password"
uvicorn main:app --reload
```

Configure `API_USERNAME` and `API_PASSWORD` before starting the API. In Replit, store both in Secrets; locally, set them as environment variables. Do not commit credentials to the project. The API runs at `http://127.0.0.1:8000`. The `users.db` SQLite file and its `users` table are created automatically the first time the API starts.

Open Swagger UI at `http://127.0.0.1:8000/docs`. FastAPI also provides the OpenAPI schema at `http://127.0.0.1:8000/openapi.json`.
Use Swagger UI's **Authorize** button to enter the same HTTP Basic Auth username and password required by the user endpoints.

## User fields

| Field | Type | Rules |
| --- | --- | --- |
| `id` | integer | Generated automatically |
| `name` | string | Required, 1–100 characters; surrounding whitespace is removed |
| `email` | string | Required, must be a valid email, and must be unique |

## API endpoints

All request and response bodies use JSON. User endpoints require HTTP Basic Auth. Send the configured username and password with your request; requests without valid credentials receive `401 Unauthorized`.

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
curl -u "$API_USERNAME:$API_PASSWORD" \
  -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex Student","email":"alex@example.com"}'
```

List users:

```bash
curl -u "$API_USERNAME:$API_PASSWORD" http://127.0.0.1:8000/users
```

Update user with ID `1`:

```bash
curl -u "$API_USERNAME:$API_PASSWORD" \
  -X PUT http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex S.","email":"alex@example.com"}'
```

Delete user with ID `1`:

```bash
curl -u "$API_USERNAME:$API_PASSWORD" \
  -X DELETE http://127.0.0.1:8000/users/1
```

### Errors

- `404 Not Found` — the requested user ID does not exist.
- `409 Conflict` — the email address is already in use.
- `422 Unprocessable Entity` — the request body is missing required fields or has an invalid name or email.
- `401 Unauthorized` — the request is missing valid Basic Auth credentials.
- `503 Service Unavailable` — `API_USERNAME` or `API_PASSWORD` is not configured.

## Run the tests

Install the dependencies, then run:

```bash
pytest
```

The tests use a temporary SQLite database and cover Basic Auth, the CRUD flow, invalid email addresses, duplicate email addresses, and missing users.

## Replit preview

The API is available through the `/api` preview prefix in this project. For example, use `/api/users` and `/api/docs` in the preview. When running the API locally with the commands above, use the unprefixed paths shown in the endpoint table.

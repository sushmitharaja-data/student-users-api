"""A beginner-friendly REST API for managing users."""

import sqlite3
from pathlib import Path
from typing import Generator

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, EmailStr, Field, field_validator


DATABASE_PATH = Path(__file__).resolve().with_name("users.db")


def create_connection() -> sqlite3.Connection:
    """Open a database connection and return rows by column name."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the users table the first time the API starts."""
    connection = create_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Provide one SQLite connection to a request and close it afterward."""
    connection = create_connection()
    try:
        yield connection
    finally:
        connection.close()


class UserFields(BaseModel):
    """Fields shared by new-user and update requests."""

    name: str = Field(min_length=1, max_length=100, description="User's name")
    email: EmailStr = Field(description="A valid email address")

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        cleaned_name = value.strip()
        if not cleaned_name:
            raise ValueError("Name cannot be blank.")
        return cleaned_name


class UserCreate(UserFields):
    """Request body for creating a user."""


class UserUpdate(UserFields):
    """Request body for replacing a user's name and email."""


class UserResponse(UserFields):
    """User data returned by the API."""

    id: int


app = FastAPI(
    title="Student Users API",
    description="A small REST API for creating, listing, updating, and deleting users.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)
users_router = APIRouter()


@users_router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
)
def create_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db)) -> UserResponse:
    try:
        cursor = db.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, str(user.email)),
        )
        db.commit()
    except sqlite3.IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from error

    return UserResponse(id=cursor.lastrowid, name=user.name, email=user.email)


@users_router.get(
    "/users",
    response_model=list[UserResponse],
    summary="List all users",
)
def list_users(db: sqlite3.Connection = Depends(get_db)) -> list[UserResponse]:
    rows = db.execute("SELECT id, name, email FROM users ORDER BY id").fetchall()
    return [
        UserResponse(id=row["id"], name=row["name"], email=row["email"])
        for row in rows
    ]


@users_router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Replace a user's name and email",
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: sqlite3.Connection = Depends(get_db),
) -> UserResponse:
    existing_user = db.execute(
        "SELECT id FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    try:
        db.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (user.name, str(user.email), user_id),
        )
        db.commit()
    except sqlite3.IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from error

    return UserResponse(id=user_id, name=user.name, email=user.email)


@users_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete a user",
)
def delete_user(user_id: int, db: sqlite3.Connection = Depends(get_db)) -> Response:
    cursor = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# The root routes match the assignment exactly. The /api aliases let the
# endpoints work through this project's Replit API preview path as well.
app.include_router(users_router)
app.include_router(users_router, prefix="/api", include_in_schema=False)


@app.get("/api/openapi.json", include_in_schema=False)
def api_openapi_schema() -> dict:
    """Serve the OpenAPI schema through the Replit API preview path."""
    return app.openapi()


@app.get("/api/docs", include_in_schema=False)
def api_swagger_docs() -> Response:
    """Serve Swagger UI through the Replit API preview path."""
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=f"{app.title} - Swagger UI",
    )


@app.get("/healthz", include_in_schema=False)
@app.get("/api/healthz", include_in_schema=False)
def health_check() -> dict[str, str]:
    return {"status": "ok"}


initialize_database()
